from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """ Hash the password securely before storing it."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Check the password against its stored hash."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Set the token expiration time.
    payload = {"sub": str(user_id), "exp": expire}  # Store the user ID and expiration in the JWT payload.
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # Sign and return the access token.


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # Verify the token and extract its payload.
        return int(payload["sub"]) # Return the user ID stored in the token.
    except Exception:
        return None
