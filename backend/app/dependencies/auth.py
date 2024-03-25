import os

from app.auth.auth0 import Auth0Client, Auth0ClientConfig

config = Auth0ClientConfig(
    auth0_domain=os.getenv("AUTH0_DOMAIN"),
    auth0_api_audience=os.getenv("AUTH0_API_AUDIENCE"),
    auth0_issuer=os.getenv("AUTH0_ISSUER"),
    auth0_algorithms=os.getenv("AUTH0_ALGORITHMS"),
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
)
# Create an instance of the Auth0Client
auth0_client = Auth0Client(config)


def get_token_verifier():
    """Get the token verifier

    Returns:
        _type_: TokenVerifier
    """
    return auth0_client.get_token_verifier()


def get_user_manager():
    """Get the user manager

    Returns:
        _type_: UserManager
    """
    return auth0_client.get_user_manager()
