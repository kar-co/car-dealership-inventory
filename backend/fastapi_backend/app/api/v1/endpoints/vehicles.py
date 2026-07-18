from decimal import Decimal
from typing import Annotated

from app.db.session import get_db
from app.dependencies.auth import get_current_admin, get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def get_vehicle_or_404(vehicle_id: int, db: Session) -> Vehicle:
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )
    return vehicle


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_admin)],
) -> Vehicle:
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.get("", response_model=list[VehicleResponse])
def list_vehicles(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
) -> list[Vehicle]:
    return db.query(Vehicle).order_by(Vehicle.id).all()


@router.get("/search", response_model=list[VehicleResponse])
def search_vehicles(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_user)],
    query: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
    min_price: Annotated[Decimal | None, Query(ge=0)] = None,
    max_price: Annotated[Decimal | None, Query(ge=0)] = None,
) -> list[Vehicle]:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="min_price cannot exceed max_price",
        )
    filters = []
    if query:
        pattern = f"%{query}%"
        filters.append(
            or_(
                Vehicle.make.ilike(pattern),
                Vehicle.model.ilike(pattern),
                Vehicle.category.ilike(pattern),
            )
        )
    if min_price is not None:
        filters.append(Vehicle.price >= min_price)
    if max_price is not None:
        filters.append(Vehicle.price <= max_price)
    return db.query(Vehicle).filter(*filters).order_by(Vehicle.id).all()


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    payload: VehicleUpdate,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_admin)],
) -> Vehicle:
    vehicle = get_vehicle_or_404(vehicle_id, db)
    for field, value in payload.model_dump().items():
        setattr(vehicle, field, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(get_current_admin)],
) -> Response:
    vehicle = get_vehicle_or_404(vehicle_id, db)
    db.delete(vehicle)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
