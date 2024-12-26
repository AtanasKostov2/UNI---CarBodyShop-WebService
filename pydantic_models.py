from pydantic import BaseModel


class GarageValidation(BaseModel):
    id: int = None  # id for response parsing and None for POST handling
    city: str
    location: str
    name: str
    capacity: int = 0

    class Config:
        from_attributes = True  # for alchemy orm


class CarValidationPOST(BaseModel):
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garageIds: list[int]

    class Config:
        from_attributes = True


class CarValidationGET(BaseModel):
    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garages: list[GarageValidation]

    class Config:
        from_attributes = True
