from pydantic import BaseModel


class GarageValidation(BaseModel):
    id: int = None  # id for response parsing and None for POST handling
    city: str
    location: str
    name: str
    capacity: int = 0

    class Config:
        from_attributes = True  # for alchemy orm
