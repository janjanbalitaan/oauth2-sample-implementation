from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CommonBase(BaseModel):
    created: datetime
    updated: datetime
    deleted: Optional[datetime]