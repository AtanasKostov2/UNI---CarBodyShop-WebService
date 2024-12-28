import calendar
from fastapi.responses import JSONResponse
from constants import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from endpoints.reports import build_monthly_report
from models import Car, Garage, Maintenance, CarGarageBridge
from pydantic_models import MaintenanceMonthlyRequestsReport, MaintenanceValidationGET, MaintenanceValidationPOST

from datetime import date
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=MaintenanceValidationGET)
def post_maintenance(maintenance: MaintenanceValidationPOST, db: Session = Depends(get_db)):
    db_garage = db.get(Garage, maintenance.garageId)
    db_car = db.get(Car, maintenance.carId)

    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    selected_car_garage_ids = [garage.id for garage in db_car.garages]
    if maintenance.garageId not in selected_car_garage_ids:
        raise HTTPException(status_code=400, detail=f"The selected car '{db_car.model}' does not belong to the selected garage '{db_garage.name}'")

    new_maintenance = Maintenance(
        carId=db_car.id,
        garageId=db_garage.id,
        serviceType=maintenance.serviceType,
        scheduledDate=maintenance.scheduledDate,
    )

    db.add(new_maintenance)
    db.commit()
    db.refresh(new_maintenance)

    return new_maintenance


@router.get("/monthlyRequestsReport", response_model=list[MaintenanceMonthlyRequestsReport])
def garage_report(
    garageId: int,
    startMonth: str,
    endMonth: str,
    db: Session = Depends(get_db),
):
    db_garage = db.get(Garage, garageId)
    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    try:
        datetime.strptime(startMonth, "%Y-%m")
        datetime.strptime(endMonth, "%Y-%m")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format passed. It should adhere to 'yyyy-mm':\n{e}")

    startMonth += "-01"
    dt = datetime.strptime(endMonth, "%Y-%m")
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    endMonth += f"-{last_day}"

    startMonth = datetime.strptime(startMonth, "%Y-%m-%d")
    endMonth = datetime.strptime(endMonth, "%Y-%m-%d")

    query = db.query(Maintenance)
    query = query.filter(Maintenance.garageId == garageId)
    query = query.filter(Maintenance.scheduledDate >= startMonth)
    query = query.filter(Maintenance.scheduledDate <= endMonth)

    available_maintenances = query.all()
    response = build_monthly_report(available_maintenances, startMonth.year, endMonth.year)
    return JSONResponse(content=response, status_code=200)


@router.put("/{maintenance_id}", response_model=MaintenanceValidationGET)
def post_maintenance(maintenance_id: int, maintenance: MaintenanceValidationPOST, db: Session = Depends(get_db)):
    db_car = db.get(Car, maintenance.carId)
    db_garage = db.get(Garage, maintenance.garageId)
    db_maintenance = db.get(Maintenance, maintenance_id)

    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    if db_maintenance is None:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    selected_car_garage_ids = [garage.id for garage in db_car.garages]
    if maintenance.garageId not in selected_car_garage_ids:
        raise HTTPException(status_code=400, detail=f"The selected car '{db_car.model}' does not belong to the selected garage '{db_garage.name}'")

    db_maintenance.carId = maintenance.carId
    db_maintenance.garageId = maintenance.garageId
    db_maintenance.serviceType = maintenance.serviceType
    db_maintenance.scheduledDate = maintenance.scheduledDate

    db.commit()
    db.refresh(db_maintenance)

    return db_maintenance


@router.get("/{maintenance_id}", response_model=MaintenanceValidationGET)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.get(Maintenance, maintenance_id)
    if maintenance is None:
        raise HTTPException(status_code=404, detail=f"Maintenance with id: {maintenance_id} not found")

    return maintenance


@router.get("/", response_model=list[MaintenanceValidationGET])
def get_maintenances(
    carId: str | None = None,
    garageId: int | None = None,
    startDate: date | None = None,
    endDate: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Maintenance)
    if startDate and endDate and startDate > endDate:
        raise HTTPException(status_code=400, detail="startDate cannot be after endDate")

    query = query.filter(Maintenance.carId == carId) if carId else query
    query = query.filter(Maintenance.garageId == garageId) if garageId else query
    query = query.filter(Maintenance.scheduledDate >= startDate) if startDate else query
    query = query.filter(Maintenance.scheduledDate <= endDate) if endDate else query

    maintenances = query.all()
    return maintenances


@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = db.get(Maintenance, maintenance_id)

    if db_maintenance is None:
        raise HTTPException(status_code=404, detail=f"Maintenance with id: {maintenance_id} not found")

    db.delete(db_maintenance)
    db.commit()

    return True
