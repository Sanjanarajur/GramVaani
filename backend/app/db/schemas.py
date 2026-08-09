from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GrievanceCreate(BaseModel):
    description: str

class GrievanceResponse(BaseModel):
    id: int
    description: str
    category: Optional[str] = None
    priority: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    solution: Optional[str] = None
    status: Optional[str] = "Pending"
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
