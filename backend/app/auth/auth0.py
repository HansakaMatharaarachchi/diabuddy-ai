from dataclasses import dataclass
from typing import List, Optional

import jwt
from auth0.authentication import GetToken
from auth0.management import Auth0
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes


@dataclass
class Auth0ClientConfig:
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: List[str]
    client_id: str
    client_secret: str


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(
        self,
        auth0_domain: str,
        auth0_api_audience: str,
        auth0_issuer: str,
        auth0_algorithms: list[str],
    ):
        self.config = {
            "auth0_domain": auth0_domain,
            "auth0_api_audience": auth0_api_audience,
            "auth0_issuer": auth0_issuer,
            "auth0_algorithms": auth0_algorithms,
        }

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f"https://{self.config['auth0_domain']}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ) -> str:
        if token is None:
            raise UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config["auth0_algorithms"],
                audience=self.config["auth0_api_audience"],
                issuer=self.config["auth0_issuer"],
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        if len(security_scopes.scopes) > 0:
            self._check_claims(payload, "scope", security_scopes.scopes)

        return payload["sub"]

    def _check_claims(self, payload, claim_name, expected_value):
        if claim_name not in payload:
            raise UnauthorizedException(
                detail=f'No claim "{claim_name}" found in token'
            )

        payload_claim = payload[claim_name]

        if claim_name == "scope":
            payload_claim = payload[claim_name].split(" ")

        for value in expected_value:
            if value not in payload_claim:
                raise UnauthorizedException(detail=f'Missing "{claim_name}" scope')


class Auth0Client:

    def __init__(self, config: Auth0ClientConfig):
        self.config = config
        self.client_id = self.config.client_id
        self.client_secret = self.config.client_secret
        self.get_token = GetToken(
            self.config.auth0_domain, self.client_id, client_secret=self.client_secret
        )
        self.mgmt_api_token = self.get_management_token()
        self.auth0 = Auth0(self.config.auth0_domain, self.mgmt_api_token)
        self.verify_token = VerifyToken(
            self.config.auth0_domain,
            self.config.auth0_api_audience,
            self.config.auth0_issuer,
            self.config.auth0_algorithms,
        )

    def get_management_token(self):
        token = self.get_token.client_credentials(
            f"https://{self.config.auth0_domain}/api/v2/"
        )
        return token["access_token"]

    def get_token_verifier(self):
        return self.verify_token

    def get_user_manager(self):
        return self.auth0.users
