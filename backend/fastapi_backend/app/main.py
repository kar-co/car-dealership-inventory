from fastapi import FastAPI

app = FastAPI(
    title="Car Dealership Inventory System API",
    description="Backend API for Car Dealership Inventory System",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Car Dealership Inventory System API"
    }