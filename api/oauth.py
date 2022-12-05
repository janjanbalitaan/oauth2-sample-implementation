from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from copy import deepcopy
from typing import Union
from datetime import datetime
from uuid import UUID
from typing import Literal, Union

from models.oauth import (
    PasswordGrantRequest, 
    PasswordGrantResponse,
    RefreshTokenGrantRequest,
    RefreshTokenGrantResponse,
)
from models.token import AddToken
from models.responses import HTTPSuccess, HTTPError
from utilities.model import Model
from utilities.db import users, tokens
from utilities.hash import Hash
from utilities.jwt import JWT, JWTBearer
from utilities.settings import Settings

oauth_router = APIRouter()
model = Model()
hash = Hash()
jwt = JWT()
settings = Settings()

@oauth_router.post(
    '/token',
    status_code=200,
    responses={
        200: {
            "model": Union[
                PasswordGrantResponse,
                RefreshTokenGrantResponse,
            ],
            "description": "successfully authenticated using password grant",
        },
        400: {
            "model": HTTPError,
            "description": "error while authenticating using password grant",
        },
    }
)
async def authenticate(
    payload: Union[
        PasswordGrantRequest,
        RefreshTokenGrantRequest,
    ]
):
    # TODO: implement scopes
    try:
        content = {
            "token_type": "bearer",
        }
        new_payload = deepcopy(payload)
        if new_payload.grant_type == "password":
            q = await model.get(
                users,
                {
                    "username": new_payload.username,
                },
            )
            if len(q) == 0:
                raise HTTPException(status_code=404, detail=f'username={new_payload.username} not found')
            
            user_id = q[0]["id"]
            username = new_payload.username
            password = new_payload.password.encode('utf-8')
            hashed_password = q[0]["password"].encode('utf-8')
            if not hash.validate_password(
                password,
                hashed_password
            ):
                raise Exception(f'user credentials are invalid')

            add_token = AddToken(
                user_id=user_id
            )
            # generate access token and refresh token
            r = await model.create(
                tokens,
                add_token,
                [
                    "token",
                    "expiration"
                ],
                is_exclude_none=True,
            )
            
            content["refresh_token"] = str(r["token"])
            content["refresh_token_expiration"] = r["expiration"].timestamp() if r["expiration"] else r["expiration"]
        elif new_payload.grant_type == "refresh_token":
            q = await model.get(
                tokens,
                {
                    "token": new_payload.refresh_token,
                },
            )
            if len(q) == 0:
                raise HTTPException(status_code=404, detail=f'refresh_token is not valid')
            
            if datetime.now() >= q[0]["expiration"]:
                raise HTTPException(status_code=403, detail=f'refresh_token is already expired')

            user_id = q[0]["user_id"]
            u = await model.get(
                users,
                {
                    "id": user_id,
                },
            )
            if len(u) == 0:
                raise HTTPException(status_code=404, detail=f'user id={user_id} does not exists')
            
            username = u[0]["username"]
            
        else:
            raise Exception(f'grant_type={new_payload.grant_type} is not yet supported')

        # generate access token
        access_token, access_token_expiration = jwt.encode(
            {
                "user_id": str(user_id),
                "username": username,
            },
            settings.secret_key,
        )
        content["access_token"] = access_token
        content["access_token_expiration"] = access_token_expiration
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    headers = {
        "Cache-Control": "no-store",
    }

    return JSONResponse(content=content, headers=headers)

@oauth_router.delete(
    '/revoke/{refresh_token}', 
    status_code=200, 
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully revoked a token"
        },
        400: {
            "model": HTTPError,
            "description": "error while revoking a token"
        },
        404: {
            "model": HTTPError,
            "description": "token does not exists"
        },
    },
)
async def revoke(
    refresh_token: UUID, 
): 
    g = await model.get(
        tokens,
        {
            "token": refresh_token,
        },
    )
    if len(g) == 0:
        raise HTTPException(status_code=404, detail=f'refresh_token is not valid')

    try:
        await model.delete(
            tokens,
            {
                "token": refresh_token,
            },
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully revoked the token'
    }

@oauth_router.delete(
    '/revoke', 
    status_code=200, 
    responses={
        200: {
            "model": HTTPSuccess,
            "description": "successfully revoked all tokens"
        },
        400: {
            "model": HTTPError,
            "description": "error while revoking all tokens"
        },
    },
    dependencies=[
        Depends(JWTBearer()),
    ]
)
async def revoke_all(
    refresh_token: Union[Literal["all"], UUID],
    access_token: str = Depends(JWTBearer())
): 
    try:
        payload = jwt.decode(
            token=access_token,
            secret=settings.secret_key,
        )
        
        user_id = payload["user_id"]
        where_c = {
            "user_id": user_id,
        }
        if refresh_token and refresh_token != "all":
            g = await model.get(
                tokens,
                {
                    "token": refresh_token,
                },
            )
            if len(g) == 0:
                raise HTTPException(status_code=404, detail=f'refresh_token is not valid')

            where_c["token"] = refresh_token
        await model.delete(
            tokens,
            where_c,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{str(e)}')

    return {
        "detail": f'successfully revoked all the tokens for a specific user'
    }