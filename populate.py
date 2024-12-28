from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DATABASE_URL
from models import Car, Garage

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session()

    try:

        garage1 = Garage(city="Plovdiv", location="Plovdiv", name="Garage01", capacity=50)
        garage2 = Garage(city="Plovdiv", location="Plovdiv", name="Garage02", capacity=30)
        garage3 = Garage(city="Sofiq", location="Sofiq", name="Garage03", capacity=10)
        garage4 = Garage(city="Sofiq", location="Sofiq", name="Garage04", capacity=70)

        car1 = Car(make="13131", model="Opel", productionYear=1999, licensePlate="23GDBR", garages=[garage1, garage2])
        car2 = Car(make="53324", model="BMW", productionYear=2011, licensePlate="5326FAS", garages=[garage3, garage4])
        car3 = Car(make="24254", model="Tesla model 3", productionYear=2024, licensePlate="SDADK24", garages=[garage1, garage4])

        db.add_all([garage1, garage2, garage3, garage4, car1, car2, car3])
        db.commit()

    finally:
        db.close()
