from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DATABASE_URL
from models import Car, Garage, Maintenance
from datetime import date

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

        main1 = Maintenance(carId=1, garageId=1, serviceType="Maintenance", scheduledDate=date(2015, 3, 1))
        main2 = Maintenance(carId=1, garageId=1, serviceType="Yearly checkup", scheduledDate=date(2016, 3, 1))
        main3 = Maintenance(carId=1, garageId=2, serviceType="Maintenance", scheduledDate=date(2018, 3, 1))
        main4 = Maintenance(carId=2, garageId=3, serviceType="Maintenance", scheduledDate=date(2019, 3, 1))
        main5 = Maintenance(carId=2, garageId=4, serviceType="Oil change", scheduledDate=date(2019, 3, 1))
        main6 = Maintenance(carId=3, garageId=1, serviceType="Yearly checkup", scheduledDate=date(2015, 3, 1))
        main7 = Maintenance(carId=3, garageId=1, serviceType="Maintenance", scheduledDate=date(2015, 3, 2))
        main8 = Maintenance(carId=3, garageId=4, serviceType="Maintenance", scheduledDate=date(2023, 3, 1))

        db.add_all([main1, main2, main3, main4, main5, main6, main7, main8])
        db.commit()
    finally:
        db.close()
