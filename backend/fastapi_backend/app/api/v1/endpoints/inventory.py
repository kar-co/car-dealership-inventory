from typing import Annotated

from app.db.session import get_db
from app.dependencies.auth import get_current_admin, get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import QuantityChange, VehicleResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vehicles", tags=["inventory"])


def get_vehicle_or_404(vehicle_id: int, db: Session) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )
    return vehicle


@router.post("/{vehicle_id}/purchase", response_model=VehicleResponse)
def purchase_vehicle(
    vehicle_id: int,
    payload: QuantityChange,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> Vehicle:
    vehicle = get_vehicle_or_404(vehicle_id, db)
    if vehicle.quantity < payload.quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Insufficient stock"
        )
    vehicle.quantity -= payload.quantity
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.post("/{vehicle_id}/restock", response_model=VehicleResponse)
def restock_vehicle(
    vehicle_id: int,
    payload: QuantityChange,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_admin)],
) -> Vehicle:
    vehicle = get_vehicle_or_404(vehicle_id, db)
    vehicle.quantity += payload.quantity
    db.commit()
    db.refresh(vehicle)
    return vehicle
