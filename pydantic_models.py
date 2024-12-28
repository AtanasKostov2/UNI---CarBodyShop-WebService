from datetime import date
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


class MaintenanceValidationGET(BaseModel):
    id: int
    carId: int
    carName: str
    serviceType: str
    scheduledDate: date
    garageId: int
    garageName: str

    class Config:
        from_attributes = True


class MaintenanceValidationPOST(BaseModel):
    carId: int
    garageId: int
    scheduledDate: date
    serviceType: str

    class Config:
        from_attributes = True
