from constants import DATABASE_URL
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Car, Garage, Maintenance
from pydantic_models import GarageValidation

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Connect to the db"""
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Home page, test test"}


@app.post("/garages", response_model=GarageValidation)
def post_garage(garage: GarageValidation, db: Session = Depends(get_db)):
    print(garage)
    db_garage = Garage(**garage.model_dump())
    db.add(db_garage)
    db.commit()
    db.refresh(db_garage)
    return db_garage


@app.get("/garages/{garage_id}", response_model=GarageValidation)
def get_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.get(Garage, garage_id)
    if garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    return garage


# ? ########### GET ALL ############
@app.get("/garages")
def get_garage(city: str | None = None, db: Session = Depends(get_db)):
    if city is None:
        garages = db.query(Garage).all()
    else:
        garages = db.query(Garage).filter(Garage.city == city).all()
        if len(garages) == 0:
            raise HTTPException(status_code=404, detail=f"Garages not found for the searched city: {city}")

    return garages


@app.put("/garages/{garage_id}", response_model=GarageValidation)
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


@app.delete("/garages/{garage_id}")
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    db_garage = db.get(Garage, garage_id)

    if not db_garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    db.delete(db_garage)
    db.commit()

    return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)
