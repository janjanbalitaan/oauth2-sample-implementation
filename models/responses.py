from pydantic import BaseModel

class HTTPSuccess(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "success"
            }
        }

class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "HTTPException raised."
            }
        }
