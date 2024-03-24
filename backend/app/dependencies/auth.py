from app.auth.auth0 import VerifyToken

# Initialize VerifyToken instance
auth = VerifyToken()


def get_auth():
    """Get VerifyToken instance.

    Returns:
        _type_: VerifyToken instance.
    """
    return auth
