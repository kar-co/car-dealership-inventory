from app.api.v1.endpoints import auth, inventory, vehicles
from fastapi import FastAPI

app = FastAPI(
    title="Car Dealership Inventory System API",
    description="Backend API for Car Dealership Inventory System",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to Car Dealership Inventory System API"}
