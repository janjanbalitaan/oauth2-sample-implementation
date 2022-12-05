from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from models.common import CommonBase

class Token(CommonBase):
    token: UUID
    # if None then the token is non-expiry
    expiration: Optional[datetime]
    user_id: UUID

class AddToken(BaseModel):
    user_id: UUID
    # if None then the token is non-expiry
    expiration: Optional[datetime]

class GetToken(Token):
    # overwrite password since we can empty password later on
    password: Optional[str]
