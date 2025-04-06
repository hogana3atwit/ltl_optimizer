from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    cube = Column(Float)
    motor_move = Column(Integer)
    origin = Column(String)
    destination = Column(String)

class Trailer(Base):
    __tablename__ = "trailers"
    id = Column(Integer, primary_key=True, index=True)
    capacity_weight = Column(Float)
    capacity_cube = Column(Float)
    utilization = Column(Float)

class ServiceCenter(Base):
    __tablename__ = "service_centers"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    location = Column(String)
    shift_schedule = Column(String)

class LoadLeg(Base):
    __tablename__ = "load_legs"
    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    from_center = Column(String)
    to_center = Column(String)
    distance = Column(Float)

class Bypass(Base):
    __tablename__ = "bypasses"
    id = Column(Integer, primary_key=True, index=True)
    skipped_centers = Column(Integer)
    motor_moves_saved = Column(Integer)
    savings_usd = Column(Float)

class DiffAnalysis(Base):
    __tablename__ = "diff_analysis"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String)
    metric_name = Column(String)
    model_value = Column(Float)
    baseline_value = Column(Float)
    delta = Column(Float)

