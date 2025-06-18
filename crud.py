from sqlalchemy.orm import Session
from geopy.distance import geodesic
from models import Address
from schemas import AddressCreate, AddressUpdate
from typing import List

def create_address(db: Session, address: AddressCreate) -> Address:
    """Create a new address in the database"""
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int) -> Address:
    """Get an address by ID"""
    return db.query(Address).filter(Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    """Get all addresses with pagination"""
    return db.query(Address).offset(skip).limit(limit).all()

def update_address(db: Session, address_id: int, address: AddressUpdate) -> Address:
    """Update an existing address"""
    db_address = get_address(db, address_id)
    if db_address is None:
        return None
    
    # Update only provided fields
    update_data = address.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_address, field, value)
    
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int) -> bool:
    """Delete an address"""
    db_address = get_address(db, address_id)
    if db_address is None:
        return False
    
    db.delete(db_address)
    db.commit()
    return True

def get_addresses_nearby(
    db: Session, 
    latitude: float, 
    longitude: float, 
    distance_km: float = 10.0
) -> List[Address]:
    """Get addresses within a specified distance from given coordinates"""
    # Get all addresses from database
    # Not efficient, will check on better solution later
    
    all_addresses = db.query(Address).all()
    
    # Filter addresses within the specified distance
    nearby_addresses = []
    target_coords = (latitude, longitude)
    
    for address in all_addresses:
        address_coords = (address.latitude, address.longitude)
        distance = geodesic(target_coords, address_coords).kilometers
        
        if distance <= distance_km:
            nearby_addresses.append(address)
    
    return nearby_addresses 