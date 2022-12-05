from typing import Optional
from pydantic import BaseModel, constr, root_validator
from uuid import UUID

from models.common import CommonBase

class UserBase(BaseModel):
    username: constr(strict=True, max_length=50)
    # TODO: validate password depends on the specification needed
    password: constr(strict=True, max_length=50)

class User(CommonBase, UserBase):
    id: UUID

class AddUser(UserBase):
    pass

class UpdateUser(BaseModel):
    username: Optional[constr(strict=True, max_length=50)]
    password: Optional[constr(strict=True, max_length=50)]

    # _check_any_of = root_validator('*', allow_reuse=True)(validator_cls.is_any_of)
    @root_validator(pre=True)
    def is_any_of_required(cls, v):
        if not any(v.values()):
            raise ValueError(f'any of the field is required {list(cls.schema()["properties"].keys())}')

        return v

class GetUser(CommonBase):
    id: UUID
    username: constr(strict=True, max_length=50)
