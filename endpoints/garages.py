from constants import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Car, Garage, Maintenance
from pydantic_models import GarageValidation


router = APIRouter()


@router.post("/", response_model=GarageValidation)
def post_garage(garage: GarageValidation, db: Session = Depends(get_db)):
    db_garage = Garage(**garage.model_dump())
    db.add(db_garage)
    db.commit()
    db.refresh(db_garage)
    return db_garage


@router.get("/{garage_id}", response_model=GarageValidation)
def get_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.get(Garage, garage_id)
    if garage is None:
        raise HTTPException(status_code=404, detail="Garage with id: {garage_id} not found")

    return garage


# ? ########### GET ALL ############
@router.get("/")
def get_garages(city: str | None = None, db: Session = Depends(get_db)):
    if city is None:
        garages = db.query(Garage).all()
    else:
        garages = db.query(Garage).filter(Garage.city == city).all()
        if len(garages) == 0:
            raise HTTPException(status_code=404, detail=f"Garages not found for the searched city: {city}")

    return garages


@router.put("/{garage_id}", response_model=GarageValidation)
def put_garage(garage_id: int, garage: GarageValidation, db: Session = Depends(get_db)):
    db_garage = db.get(Garage, garage_id)
    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    db_garage.city = garage.city
    db_garage.location = garage.location
    db_garage.name = garage.name
    db_garage.capacity = garage.capacity

    db.commit()
    db.refresh(db_garage)

    return db_garage


@router.delete("/{garage_id}")
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    db_garage = db.get(Garage, garage_id)

    if not db_garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    db.delete(db_garage)
    db.commit()

    return True
