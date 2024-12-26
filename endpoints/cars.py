from constants import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Car, Garage, Maintenance
from pydantic_models import CarValidationPOST, CarValidationGET


router = APIRouter()


@router.post("/", response_model=CarValidationGET)
def post_car(car: CarValidationPOST, db: Session = Depends(get_db)):

    garages = db.query(Garage).filter(Garage.id.in_(car.garageIds)).all()

    if len(garages) != len(car.garageIds):
        raise HTTPException(status_code=404, detail="Garages not found")

    new_car = Car(
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
    )
    new_car.garages = garages

    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@router.get("/{car_id}", response_model=CarValidationGET)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail=f"Car with id: {car_id} not found")

    return car


# ? ########### GET ALL ############
@router.get("/", response_model=list[CarValidationGET])
def get_cars(db: Session = Depends(get_db)):
    cars = db.query(Garage).all()

    return cars
