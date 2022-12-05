from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from utilities.db import metadata, database, engine
from utilities.settings import Settings

# routers
from api.generic import generic
from api.user import user_router
from api.oauth import oauth_router

metadata.create_all(engine)
settings = Settings()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# TODO: update this for security purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

# routes
app.include_router(oauth_router, prefix='/api/oauth2', tags=["oauth2"])
app.include_router(generic, prefix='/api/generic', tags=["generic"])
app.include_router(user_router, prefix='/api/users', tags=["users"])
