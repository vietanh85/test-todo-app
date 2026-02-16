import pytest
import respx
import httpx
from auth import TokenValidator
from jose import jwt
from fastapi import HTTPException
import time

@pytest.mark.asyncio
async def test_token_validator_discovery():
    issuer = "https://test-issuer.com"
    jwks_uri = "https://test-issuer.com/jwks"
    
    with respx.mock:
        respx.get(f"{issuer}/.well-known/openid-configuration").mock(
            return_value=httpx.Response(200, json={"jwks_uri": jwks_uri})
        )
        
        # We need to set the environment variable or patch it
        import auth
        original_issuer = auth.OIDC_ISSUER
        auth.OIDC_ISSUER = issuer
        auth.JWKS_URL = None
        
        validator = TokenValidator()
        discovered_url = await validator._fetch_jwks_url()
        assert discovered_url == jwks_uri
        
        auth.OIDC_ISSUER = original_issuer

@pytest.mark.asyncio
async def test_token_validator_get_jwks():
    jwks_url = "https://test-issuer.com/jwks"
    jwks_data = {"keys": [{"kid": "1", "kty": "RSA", "n": "...", "e": "AQAB", "use": "sig"}]}
    
    with respx.mock:
        respx.get(jwks_url).mock(
            return_value=httpx.Response(200, json=jwks_data)
        )
        
        import auth
        auth.JWKS_URL = jwks_url
        
        validator = TokenValidator()
        jwks = await validator.get_jwks()
        assert jwks == jwks_data
        assert validator.jwks == jwks_data
        
@pytest.mark.asyncio
async def test_token_validator_validate_token_success(mocker):
    # Mock JWKS
    jwks_data = {
        "keys": [
            {"kid": "test-kid", "kty": "RSA", "n": "...", "e": "AQAB", "use": "sig"}
        ]
    }
    
    import auth
    auth.OIDC_ISSUER = "https://test-issuer.com"
    auth.OIDC_AUDIENCE = "test-audience"
    
    validator = TokenValidator()
    # Mock get_jwks to return our test data
    mocker.patch.object(validator, 'get_jwks', return_value=jwks_data)
    
    # Mock jwt.get_unverified_header and jwt.decode
    mocker.patch('jose.jwt.get_unverified_header', return_value={"kid": "test-kid"})
    decoded_payload = {"sub": "user-123", "email": "user@example.com"}
    mocker.patch('jose.jwt.decode', return_value=decoded_payload)
    
    payload = await validator.validate_token("fake-token")
    assert payload == decoded_payload

@pytest.mark.asyncio
async def test_token_validator_validate_token_invalid_kid(mocker):
    jwks_data = {"keys": [{"kid": "other-kid", "kty": "RSA", "n": "...", "e": "AQAB", "use": "sig"}]}
    
    import auth
    auth.OIDC_ISSUER = "https://test-issuer.com"
    
    validator = TokenValidator()
    mocker.patch.object(validator, 'get_jwks', side_effect=[jwks_data, jwks_data])
    mocker.patch('jose.jwt.get_unverified_header', return_value={"kid": "test-kid"})
    
    with pytest.raises(HTTPException) as exc:
        await validator.validate_token("fake-token")
    assert exc.value.status_code == 401
    assert "Public key not found in JWKS" in str(exc.value.detail)

