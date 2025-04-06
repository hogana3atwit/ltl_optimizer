from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, crud, database, schemas
from app.ml import optimizer
from app.routing.engine import route_shipment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the LTL Optimizer App"}

@app.get("/shipments", response_model=list[schemas.ShipmentResponse])
def get_shipments(db: Session = Depends(database.get_db)):
    return crud.get_all_shipments(db)

@app.post("/shipments", response_model=schemas.ShipmentResponse)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(database.get_db)):
    db_shipment = models.Shipment(**shipment.dict())
    return crud.create_shipment(db, db_shipment)

@app.get("/trailers", response_model=list[schemas.TrailerResponse])
def get_trailers(db: Session = Depends(database.get_db)):
    return crud.get_all_trailers(db)

@app.post("/trailers", response_model=schemas.TrailerResponse)
def create_trailer(trailer: schemas.TrailerCreate, db: Session = Depends(database.get_db)):
    db_trailer = models.Trailer(**trailer.dict())
    return crud.create_trailer(db, db_trailer)

@app.get("/service_centers", response_model=list[schemas.ServiceCenterResponse])
def get_service_centers(db: Session = Depends(database.get_db)):
    return crud.get_all_service_centers(db)

@app.post("/service_centers", response_model=schemas.ServiceCenterResponse)
def create_service_center(center: schemas.ServiceCenterCreate, db: Session = Depends(database.get_db)):
    db_center = models.ServiceCenter(**center.dict())
    return crud.create_service_center(db, db_center)

@app.get("/bypasses", response_model=list[schemas.BypassResponse])
def get_bypasses(db: Session = Depends(database.get_db)):
    return crud.get_all_bypasses(db)

@app.post("/bypasses", response_model=schemas.BypassResponse)
def create_bypass(bypass: schemas.BypassCreate, db: Session = Depends(database.get_db)):
    db_bypass = models.Bypass(**bypass.dict())
    return crud.create_bypass(db, db_bypass)

@app.get("/load_legs", response_model=list[schemas.LoadLegResponse])
def get_load_legs(db: Session = Depends(database.get_db)):
    return crud.get_all_load_legs(db)

@app.post("/load_legs", response_model=schemas.LoadLegResponse)
def create_load_leg(load_leg: schemas.LoadLegCreate, db: Session = Depends(database.get_db)):
    db_load_leg = models.LoadLeg(**load_leg.dict())
    return crud.create_load_leg(db, db_load_leg)

@app.get("/predict_utilization")
def predict_utilization(weight: float, cube: float):
    model = optimizer.load_model()
    prediction = optimizer.predict_utilization(model, weight, cube)
    return {"predicted_utilization": prediction}

@app.post("/train_model")
def train_model():
    try:
        model = optimizer.train_utilization_model("data/sample_data.csv")
        return {"message": "Model trained successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/route_shipment")
def route_shipment_api(shipment: dict):
    try:
        return route_shipment(shipment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
