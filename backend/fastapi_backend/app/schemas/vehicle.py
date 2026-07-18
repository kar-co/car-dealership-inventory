from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    make: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    quantity: int = Field(ge=0)


class VehicleUpdate(VehicleCreate):
    pass


class QuantityChange(BaseModel):
    quantity: int = Field(gt=0)


class VehicleResponse(VehicleCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
