from constants import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Car, Garage, Maintenance, CarGarageBridge
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
        garages=garages,
    )

    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return new_car


@router.put("/{car_id}", response_model=CarValidationGET)
def post_put(car_id: int, car: CarValidationPOST, db: Session = Depends(get_db)):
    db_car = db.get(Car, car_id)
    garages = db.query(Garage).filter(Garage.id.in_(car.garageIds)).all()

    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    if len(garages) != len(car.garageIds):
        raise HTTPException(status_code=404, detail="Garages not found")

    db_car.make = car.make
    db_car.model = car.model
    db_car.productionYear = car.productionYear
    db_car.licensePlate = car.licensePlate
    db_car.garages = garages

    db.commit()
    db.refresh(db_car)

    return db_car


@router.get("/{car_id}", response_model=CarValidationGET)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail=f"Car with id: {car_id} not found")

    return car


@router.get("/", response_model=list[CarValidationGET])
def get_cars(
    carMake: str | None = None,
    garageId: int | None = None,
    fromYear: int | None = None,
    toYear: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Car)

    if carMake:
        query = query.filter(Car.make == carMake)

    if fromYear:
        query = query.filter(Car.productionYear >= fromYear)

    if toYear:
        query = query.filter(Car.productionYear <= toYear)

    if garageId:
        query = query.join(CarGarageBridge).filter(CarGarageBridge.garageId == garageId)
        # car.id for car in cars for garage in car.garages if garage.id == garageId

    cars = query.all()
    return cars


@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.get(Car, car_id)

    if db_car is None:
        raise HTTPException(status_code=404, detail=f"Car with id: {car_id} not found")

    db.delete(db_car)
    db.commit()

    return True
