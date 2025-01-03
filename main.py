from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from endpoints import garages, cars, maintenances

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(garages.router, prefix="/garages", tags=["Garages"])
app.include_router(cars.router, prefix="/cars", tags=["Cars"])
app.include_router(maintenances.router, prefix="/maintenance", tags=["Maintenances"])


@app.get("/")
def home():
    return {"message": "Home page, test test"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8088, reload=True)
