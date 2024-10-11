from uuid import uuid4
import jwt

from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from api.core.entities import (
    RefreshToken,
    User,
    AccessJWTTokenData,
    AccessToken,
    RefreshTokenId,
)


class AuthService:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        secret_key: str,
        access_token_min: int,
        refresh_token_days: int,
    ):
        self._secret_key = secret_key
        self._access_token_min = access_token_min
        self._refresh_token_days = refresh_token_days

    def hash_pass(self, raw_password: str) -> str:
        return self._pwd_context.hash(raw_password)

    def verify_pass(self, raw_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(raw_password, hashed_password)

    def create_access_token(self, user: User) -> AccessToken:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=self._access_token_min
        )
        jwt_token_data = AccessJWTTokenData(
            user_id=user.id, role=user.role, expires_at=expires_at, token=""
        )

        payload = {
            "user_id": 123,
            "role": user.role,
            "expires_at": expires_at,
        }
        token = jwt.encode(payload, self._secret_key, algorithm="HS256")
        jwt_token_data.token = token

        access_token = AccessToken(
            user_id=user.id,
            jwt_token_data=jwt_token_data,
            expires_at=expires_at,
        )

        return access_token

    def parse_access_token(self, jwt_token: str):
        try:
            decoded_payload = jwt.decode(
                jwt_token, self._secret_key, algorithms=["HS256"]
            )

            user_id = decoded_payload.get("user_id")
            role = decoded_payload.get("role")
            expires_at = decoded_payload.get("expires_at")

            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)

            access_token = AccessToken(
                user_id=user_id,
                jwt_token_data=AccessJWTTokenData(
                    user_id=user_id,
                    role=role,
                    expires_at=expires_at,
                    token=jwt_token,
                ),
                expires_at=expires_at,
            )

            return access_token
        except Exception:  # FIXME: потому что надо, михей потом разберется.
            raise ValueError("Invalid token")

    def create_refresh_token(self, user_id):
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self._refresh_token_days
        )
        id = RefreshTokenId(uuid4())

        refresh_token = RefreshToken(
            id=id,
            user_id=user_id,
            expires_at=expires_at,
            issued_at=datetime.now(timezone.utc),
        )

        return refresh_token
