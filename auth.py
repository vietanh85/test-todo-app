import os
import httpx
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# Configuration
OIDC_ISSUER = os.getenv("OIDC_ISSUER")
OIDC_AUDIENCE = os.getenv("OIDC_AUDIENCE")
JWKS_URL = os.getenv("JWKS_URL")

security = HTTPBearer()

class AuthUser(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

class TokenValidator:
    def __init__(self):
        self.jwks: Optional[Dict[str, Any]] = None

    async def get_jwks(self) -> Dict[str, Any]:
        if self.jwks is None:
            if not JWKS_URL:
                raise ValueError("JWKS_URL environment variable is not set")
            async with httpx.AsyncClient() as client:
                response = await client.get(JWKS_URL)
                response.raise_for_status()
                self.jwks = response.json()
        
        if self.jwks is None:
            raise ValueError("Failed to fetch JWKS")
            
        return self.jwks

    async def validate_token(self, token: str) -> Dict[str, Any]:
        try:
            jwks = await self.get_jwks()
            unverified_header = jwt.get_unverified_header(token)
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
            
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=OIDC_AUDIENCE,
                    issuer=OIDC_ISSUER
                )
                return payload
        except JWTError as e:
            logger.error(f"JWT validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Unexpected error validating token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during authentication"
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

validator = TokenValidator()

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> AuthUser:
    """
    Dependency to get the current authenticated user from JWT.
    """
    if not OIDC_ISSUER or not OIDC_AUDIENCE or not JWKS_URL:
        # For development purposes, if SSO is not configured, we might want to skip validation
        # or raise an error. Given the "senior developer" role, I'll raise an error.
        logger.error("SSO environment variables are not set")
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
    
    return AuthUser(
        id=user_id,
        email=email,
        name=payload.get("name"),
        picture=payload.get("picture")
    )
