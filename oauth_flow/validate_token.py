import requests
import time
import os

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

METADATA_URL = "https://login.eveonline.com/.well-known/oauth-authorization-server"
METADATA_CACHE_TIME = 300  # 5 minutes
ACCEPTED_ISSUERS = ("logineveonline.com", "https://login.eveonline.com")
EXPECTED_AUDIENCE = "EVE Online"
CLIENT_ID = os.getenv("EVE_CLIENT_ID", "")

# We don't want to fetch the jwks data on every request, so we cache it for a short period
JWKS_METADATA = None
JWKS_METADATA_TTL = 0


def fetch_jwks_metadata():
    """
    Fetches the JWKS metadata from the SSO server.

    :returns: The JWKS metadata
    """
    global JWKS_METADATA, JWKS_METADATA_TTL
    if JWKS_METADATA is None or JWKS_METADATA_TTL < time.time():
        resp = requests.get(METADATA_URL)
        resp.raise_for_status()
        metadata = resp.json()

        jwks_uri = metadata["jwks_uri"]

        resp = requests.get(jwks_uri)
        resp.raise_for_status()

        JWKS_METADATA = resp.json()
        JWKS_METADATA_TTL = time.time() + METADATA_CACHE_TIME
    return JWKS_METADATA


def validate_jwt_token(token):
    """
    Validates a JWT Token.

    :param str token: The JWT token to validate
    :returns: The content of the validated JWT access token
    :raises ExpiredSignatureError: If the token has expired
    :raises JWTError: If the token is invalid
    """
    metadata = fetch_jwks_metadata()
    keys = metadata["keys"]
    # Fetch the key algorithm and key idfentifier from the token header
    header = jwt.get_unverified_header(token)
    key = [
        item
        for item in keys
        if item["kid"] == header["kid"] and item["alg"] == header["alg"]
    ].pop()
    return jwt.decode(
        token,
        key=key,
        algorithms=header["alg"],
        issuer=ACCEPTED_ISSUERS,
        audience=EXPECTED_AUDIENCE,
    )


def is_token_valid(token):
    """
    Simple check if the token is valid or not.

    :returns: True if the token is valid, False otherwise
    :returns: The claim dictionary
    """
    try:
        claims = validate_jwt_token(token)
        # If our client_id is in the audience list, the token is valid, otherwise, we got a token for another client.
        return CLIENT_ID in claims["aud"], claims
    except ExpiredSignatureError:
        print("The token has expired, re-login")
        # The token has expired
        return False, {}
    except JWTError:
        # The token is invalid
        print("This token has been denied)")
        return False, {}
    except Exception as e:
        print(f"Something went wrong? {e}")
        return False, {}