from constants import DATABASE_URL
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine

from models import Car, Garage, Maintenance
from pydantic_models import GarageValidation

from fastapi.middleware.cors import CORSMiddleware
import garages

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(garages.router, prefix="/garages", tags=["Garages"])


@app.get("/")
def home():
    return {"message": "Home page, test test"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)
