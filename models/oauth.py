from typing import Optional, List
from pydantic import BaseModel, constr

class CommonResponse(BaseModel):
    access_token: str
    access_token_expiration: float
    token_type: constr(strict=True, min_length=6, max_length=6, regex="bearer")

class PasswordGrantRequest(BaseModel):
    grant_type: constr(strict=True, min_length=8, max_length=8, regex="password")
    username: constr(strict=True, max_length=50)
    password: constr(strict=True, max_length=50)
    # TODO: scope to be implemented
    scope: Optional[List[constr(strict=True, max_length=20)]]

class PasswordGrantResponse(CommonResponse):
    refresh_token: str
    refresh_token_expiration: float

class RefreshTokenGrantRequest(BaseModel):
    grant_type: constr(strict=True, min_length=13, max_length=13, regex="refresh_token")
    refresh_token: str
    # TODO: scope to be implemented
    scope: Optional[List[constr(strict=True, max_length=20)]]

class RefreshTokenGrantResponse(CommonResponse):
    access_token: str
    access_token_expiration: float
    token_type: constr(strict=True, min_length=8, max_length=8, regex="bearer")