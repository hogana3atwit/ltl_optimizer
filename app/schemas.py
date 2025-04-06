from pydantic import BaseModel

class ShipmentBase(BaseModel):
    weight: float
    cube: float
    motor_move: int
    origin: str
    destination: str

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentResponse(ShipmentBase):
    id: int

    class Config:
        orm_mode = True

class TrailerBase(BaseModel):
    capacity_weight: float
    capacity_cube: float
    utilization: float

class TrailerCreate(TrailerBase):
    pass

class TrailerResponse(TrailerBase):
    id: int

    class Config:
        orm_mode = True

class ServiceCenterBase(BaseModel):
    code: str
    location: str
    shift_schedule: str

class ServiceCenterCreate(ServiceCenterBase):
    pass

class ServiceCenterResponse(ServiceCenterBase):
    id: int

    class Config:
        orm_mode = True

class BypassBase(BaseModel):
    skipped_centers: int
    motor_moves_saved: int
    savings_usd: float

class BypassCreate(BypassBase):
    pass

class BypassResponse(BypassBase):
    id: int

    class Config:
        orm_mode = True

class LoadLegBase(BaseModel):
    shipment_id: int
    from_center: str
    to_center: str
    distance: float

class LoadLegCreate(LoadLegBase):
    pass

class LoadLegResponse(LoadLegBase):
    id: int

    class Config:
        orm_mode = True
