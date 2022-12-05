from typing import Dict, Any, Tuple, Optional
import jwt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utilities.settings import Settings

class JWT:

    def encode(
        self,
        payload: Dict[str, Any],
        secret: str,
        algorithm: str = "HS256"
    ) -> Tuple[str, float]: 
        # add exp value on payload
        # TODO: update to utc time later on
        payload["exp"] = (datetime.now() + timedelta(minutes=30)).timestamp()
        return jwt.encode(
            payload,
            secret,
            algorithm,
        ), payload["exp"]

    def decode(
        self,
        token: str,
        secret: str,
        algorithm: str = "HS256"
    ) -> Dict[str, Any]: 
        return jwt.decode(
            token,
            secret,
            algorithm,
        )

class JWTBearer(HTTPBearer):
    jwt = JWT()
    settings = Settings()

    def __init__(
        self,
        auto_error: bool = True
    ):
        super(
            JWTBearer,
            self
        ).__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
    ):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer,
            self,
        ).__call__(
            request
        )

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )

            is_valid, message = self.is_valid_jwt(
                token=credentials.credentials,
            )

            if not is_valid:
                raise HTTPException(
                    status_code=403,
                    detail=message,
                )

        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid authorization code."
            )
        return credentials.credentials

    def is_valid_jwt(
        self,
        token: str,
    ) -> Tuple[bool, Optional[str]]:
        is_valid: bool = True
        message = None
        try:
            payload = self.jwt.decode(
                token=token,
                secret=self.settings.secret_key,
            )

            # expire 15 seconds before
            if payload["exp"] <= (datetime.now() - timedelta(seconds=15)).timestamp():
                is_valid = False
                message = "jwt token already expired."

            # TODO: other jwt validation
        except Exception as e:
            is_valid = False
            message = f'jwt token is invalid: {str(e)}'

        return is_valid, message