from pyexpat import model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, declarative_base
from constants import DATABASE_URL

Base = declarative_base()


class Garage(Base):
    __tablename__ = "Garage"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    location = Column(String, nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False, default=0)

    cars = relationship("CarGarageBridge", back_populates="garage")

    @property
    def available(self):
        return self.capacity - len(self.maintenances)


class Car(Base):
    __tablename__ = "Car"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    make = Column(String, nullable=False)  # ???
    model = Column(String, nullable=False)
    productionYear = Column(Integer, nullable=False)
    licensePlate = Column(String, nullable=False)

    garages = relationship("CarGarageBridge", back_populates="car")


class CarGarageBridge(Base):
    """Implements many-to-many relationship between Car and Garages"""

    __tablename__ = "CarGarageBridge"
    id = Column(Integer, primary_key=True)
    carId = Column(Integer, ForeignKey("Car.id"), nullable=False)
    garageId = Column(Integer, ForeignKey("Garage.id"), nullable=False)

    car = relationship("Car", back_populates="garages")
    garage = relationship("Garage", back_populates="cars")


class Maintenance(Base):
    __tablename__ = "Maintenance"

    id = Column(Integer, primary_key=True)
    carId = Column(Integer, ForeignKey("Car.id"), nullable=False)
    garageId = Column(Integer, ForeignKey("Garage.id"), nullable=False)
    serviceType = Column(String, nullable=False)
    scheduledDate = Column(Date, nullable=False)

    garage = relationship("Garage", backref="maintenances")
    car = relationship("Car", backref="maintenances")

    @property
    def garage_name(self) -> str:
        return self.garage.name

    @property
    def car_name(self) -> str:
        return self.car.name


# Create a connection to the db
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# # Delete all data
# Base.metadata.drop_all(engine)

# Create tables
Base.metadata.create_all(bind=engine)


##########################
# alembic migrations update:
# alembic revision --autogenerate -m "comment"
# alembic upgrade head
