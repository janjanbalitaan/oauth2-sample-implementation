from fastapi import Header, APIRouter
from utilities.settings import Settings

settings = Settings()
generic = APIRouter()

@generic.get('/check')
async def service_check():
    return {
        "detail": f"The {settings.app_name} is up and running"
    }
