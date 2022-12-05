from typing import List, Optional
from asyncpg import UniqueViolationError
from fastapi import APIRouter, HTTPException, Depends
from copy import deepcopy
from uuid import UUID
from pydantic import NonNegativeInt

from models.user import User, AddUser, UpdateUser, GetUser
from models.responses import HTTPSuccess, HTTPError
from utilities.model import Model
from utilities.db import users as table
from utilities.hash import Hash
from utilities.jwt import JWTBearer

user_router = APIRouter()
model = Model()
hash = Hash()

@user_router.post(
    '',
    status_code=201,
    responses={
        201: {
            "model": GetUser,
            "description": "successfully created a user",
        },
        400: {
            "model": HTTPError,
            "description": "error while creating a user",
        },
        409: {
            "model": HTTPError,
            "description": "user is already existing",
        },
    }
)
async def create(
    payload: AddUser
):
    try:
        new_payload = deepcopy(payload)
        new_payload.password = hash.hash_password(
            payload.password.encode('utf-8')
        ).decode('utf-8')
        q = await model.create(
            table,
            new_payload,
            [
                "id",
                "created",
                "updated",
                "deleted",
            ]
        )
    except UniqueViolationError:
        raise HTTPException(status_code=409, detail=f'username={payload.username} already exists')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')
        
    return {
        **q,
        "username": payload.username
    }

# TODO: validate using bearer token
@user_router.get(
    '', 
    response_model=List[GetUser],
    dependencies=[
        Depends(JWTBearer()),
    ]
)
async def get(
    id: Optional[UUID] = None, 
    username: Optional[str] = None,
    limit: Optional[NonNegativeInt] = 30,
    offset: Optional[NonNegativeInt] = 0
): 
    filters = dict()
    if id is not None:
        filters["id"] = id
    if username is not None:
        filters["username"] = username

    return await model.get(
        table,
        filters,
        limit,
        offset
    )

# TODO: validate using bearer token
@user_router.put(
    '/{id}', 
    status_code=200, 
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "user updated successfully"
        },
        400: {
            "model": HTTPError,
            "description": "error while updating a user"
        },
        409: {
            "model": HTTPError,
            "description": "user is already existing"
        },
    },
    dependencies=[
        Depends(JWTBearer()),
    ]
)
async def update(
    id: UUID, 
    payload: UpdateUser
): 
    g = await model.get(
        table,
        {
            "id": id,
        },
    )
    if len(g) == 0:
        raise HTTPException(status_code=404, detail=f'user {id=} not found')

    try:
        new_payload = deepcopy(payload)
        if g[0].username == new_payload.username:
            raise Exception(f'nothing to update on the username={payload.username}')
        if new_payload.password:
            new_payload.password = hash.hash_password(
                payload.password.encode('utf-8')
            ).decode('utf-8')
        
        await model.update(
            table,
            {
                "id": id,
            },
            new_payload,
            is_exclude_none=True,
        )
    except UniqueViolationError:
        raise HTTPException(status_code=409, detail=f'username={payload.username or g[0].username} already exists')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully updated {id=}'
    }

# TODO: validate using bearer token
@user_router.delete(
    '/{id}', 
    status_code=200, 
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully deleted a user"
        },
        400: {
            "model": HTTPError,
            "description": "error while deleting a user"
        },
        404: {
            "model": HTTPError,
            "description": "user does not exists"
        },
    },
    dependencies=[
        Depends(JWTBearer()),
    ]
)
async def delete(
    id: UUID, 
): 
    g = await model.get(
        table,
        {
            "id": id,
        },
    )
    if len(g) == 0:
        raise HTTPException(status_code=404, detail=f'{id=} not found')

    try:
        await model.delete(
            table,
            {
                "id": id,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully deleted {id=}'
    }



