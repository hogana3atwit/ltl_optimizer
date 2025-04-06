from sqlalchemy.orm import Session
from app import models

def get_all_shipments(db: Session):
    return db.query(models.Shipment).all()

def create_shipment(db: Session, shipment: models.Shipment):
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment

def get_all_trailers(db: Session):
    return db.query(models.Trailer).all()

def create_trailer(db: Session, trailer: models.Trailer):
    db.add(trailer)
    db.commit()
    db.refresh(trailer)
    return trailer

def get_all_service_centers(db: Session):
    return db.query(models.ServiceCenter).all()

def create_service_center(db: Session, center: models.ServiceCenter):
    db.add(center)
    db.commit()
    db.refresh(center)
    return center

def get_all_bypasses(db: Session):
    return db.query(models.Bypass).all()

def create_bypass(db: Session, bypass: models.Bypass):
    db.add(bypass)
    db.commit()
    db.refresh(bypass)
    return bypass

def get_all_load_legs(db: Session):
    return db.query(models.LoadLeg).all()

def create_load_leg(db: Session, load_leg: models.LoadLeg):
    db.add(load_leg)
    db.commit()
    db.refresh(load_leg)
    return load_leg
