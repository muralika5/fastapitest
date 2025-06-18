from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
import crud
from database import SessionLocal, engine
from geopy.distance import geodesic

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Address Book API",
    description="A FastAPI application for managing addresses with coordinates",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/address/add/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """Create a new address"""
    return crud.create_address(db=db, address=address)

@app.get("/address/list/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all addresses with pagination"""
    addresses = crud.get_addresses(db, skip=skip, limit=limit)
    return addresses

@app.get("/address/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(get_db)):
    """Get a specific address by ID"""
    address = crud.get_address(db, address_id=address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@app.put("/address/update/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    """Update an existing address"""
    updated_address = crud.update_address(db, address_id=address_id, address=address)
    if updated_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated_address

@app.delete("/address/delete/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """Delete an address"""
    success = crud.delete_address(db, address_id=address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}

@app.get("/address/list/nearby/", response_model=List[schemas.Address])
def get_addresses_nearby(
    latitude: float,
    longitude: float,
    distance_km: float = 10.0,
    db: Session = Depends(get_db)
):
    """Get addresses within a specified distance from given coordinates"""
    addresses = crud.get_addresses_nearby(
        db, 
        latitude=latitude, 
        longitude=longitude, 
        distance_km=distance_km
    )
    return addresses 