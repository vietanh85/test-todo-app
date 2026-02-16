import os
import httpx
import time
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
from models import AuthUser
from sqlalchemy import select
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database components
# We import inside the function or use a late import to avoid issues if needed,
# but here it should be fine.
from database import db, UserDB

logger = logging.getLogger(__name__)


# Configuration
OIDC_ISSUER = os.getenv("OIDC_ISSUER")
OIDC_AUDIENCE = os.getenv("OIDC_AUDIENCE")
JWKS_URL = os.getenv("JWKS_URL")

security = HTTPBearer()

class TokenValidator:
    """
    Handles JWT validation using JWKS from an OIDC provider.
    Includes caching and automatic discovery of JWKS URL.
    """
    def __init__(self):
        self.jwks: Optional[Dict[str, Any]] = None
        self.jwks_last_fetched: float = 0
        self.jwks_ttl: int = 3600  # Cache JWKS for 1 hour

    async def _fetch_jwks_url(self) -> str:
        """
        Discover JWKS URL from OIDC Issuer if not explicitly provided.
        Uses the .well-known/openid-configuration endpoint.
        """
        if JWKS_URL:
            return JWKS_URL
        
        if not OIDC_ISSUER:
            raise ValueError("OIDC_ISSUER environment variable is not set")
        
        config_url = f"{OIDC_ISSUER.rstrip('/')}/.well-known/openid-configuration"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(config_url)
                response.raise_for_status()
                config = response.json()
                return config["jwks_uri"]
        except Exception as e:
            logger.error(f"Failed to discover OIDC configuration from {config_url}: {e}")
            raise ValueError(f"Could not discover JWKS URL: {e}")

    async def get_jwks(self) -> Dict[str, Any]:
        """
        Retrieve JWKS (JSON Web Key Set) from the IdP.
        Implements caching based on jwks_ttl.
        """
        now = time.time()
        if self.jwks is None or (now - self.jwks_last_fetched) > self.jwks_ttl:
            jwks_url = await self._fetch_jwks_url()
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(jwks_url)
                    response.raise_for_status()
                    self.jwks = response.json()
                    self.jwks_last_fetched = now
                    logger.info("Successfully fetched and cached JWKS")
            except Exception as e:
                if self.jwks:
                    logger.warning(f"Failed to refresh JWKS, using cached version: {e}")
                else:
                    logger.error(f"Failed to fetch JWKS from {jwks_url}: {e}")
                    raise ValueError(f"Failed to fetch JWKS: {e}")
            
        assert self.jwks is not None
        return self.jwks

    async def validate_token(self, token: str) -> Dict[str, Any]:
        """Validate JWT token against JWKS"""
        try:
            jwks = await self.get_jwks()
            unverified_header = jwt.get_unverified_header(token)
            
            if "kid" not in unverified_header:
                raise JWTError("Token header missing 'kid'")
            
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    break
            
            if not rsa_key:
                # If key not found, try refreshing JWKS once
                self.jwks = None
                jwks = await self.get_jwks()
                for key in jwks["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        rsa_key = {
                            "kty": key["kty"],
                            "kid": key["kid"],
                            "use": key["use"],
                            "n": key["n"],
                            "e": key["e"]
                        }
                        break
            
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=OIDC_AUDIENCE,
                    issuer=OIDC_ISSUER
                )
                return payload
            
            raise JWTError("Public key not found in JWKS")
            
        except JWTError as e:
            logger.error(f"JWT validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Unexpected error validating token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during authentication"
            )

validator = TokenValidator()

async def sync_user(user: AuthUser):
    """Sync user info with database"""
    try:
        async with db.session() as session:
            result = await session.execute(select(UserDB).where(UserDB.id == user.id))
            db_user = result.scalar_one_or_none()
            
            current_time = datetime.now()
            
            if not db_user:
                db_user = UserDB(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    picture=user.picture,
                    last_login=current_time
                )
                session.add(db_user)
                await session.commit()
                logger.info(f"Created new user in database: {user.id}")
            else:
                # Only update if info changed or last_login is more than 5 minutes ago
                info_changed = (
                    db_user.email != user.email or 
                    db_user.name != user.name or 
                    db_user.picture != user.picture
                )
                time_to_update = not db_user.last_login or (current_time - db_user.last_login).total_seconds() > 300
                
                if info_changed or time_to_update:
                    db_user.email = user.email
                    db_user.name = user.name
                    db_user.picture = user.picture
                    db_user.last_login = current_time
                    await session.commit()
                    logger.debug(f"Updated user info/last_login: {user.id}")
                    
    except Exception as e:
        logger.error(f"Failed to sync user {user.id}: {e}")
        # We don't raise here to not block the request if user sync fails,
        # UNLESS we have foreign key constraints that would cause failures later.
        # Given we added a ForeignKey, maybe we SHOULD raise or handle it.
        # But if the DB is down, the whole request will fail anyway.

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> AuthUser:
    """
    Dependency to get the current authenticated user from JWT.
    """
    if not OIDC_ISSUER or not OIDC_AUDIENCE:
        logger.error("SSO environment variables (OIDC_ISSUER/OIDC_AUDIENCE) are not set")
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="SSO authentication not configured on server"
        )

    payload = await validator.validate_token(token.credentials)
    
    user_id = payload.get("sub")
    email = payload.get("email")
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing sub or email claim",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = AuthUser(
        id=user_id,
        email=email,
        name=payload.get("name"),
        picture=payload.get("picture")
    )
    
    # Sync user to database
    await sync_user(user)
    
    return user
