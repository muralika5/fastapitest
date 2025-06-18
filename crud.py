from sqlalchemy.orm import Session
from geopy.distance import geodesic
from models import Address
from schemas import AddressCreate, AddressUpdate
from typing import List
from math import radians, sin, cos, sqrt, atan2


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
    """
    Efficiently get addresses within a given distance using bounding box + Haversine
    """
    # Rough bounding box in degrees
    lat_range = distance_km / 111  # 1 deg ≈ 111km
    lon_range = distance_km / (111 * cos(radians(latitude)))

    min_lat = latitude - lat_range
    max_lat = latitude + lat_range
    min_lon = longitude - lon_range
    max_lon = longitude + lon_range

    # Pre-filter using bounding box in SQL
    candidate_addresses = db.query(Address).filter(
        Address.latitude.between(min_lat, max_lat),
        Address.longitude.between(min_lon, max_lon)
    ).all()

    # Apply Haversine for exact match
    nearby_addresses = [
        addr for addr in candidate_addresses
        if haversine(latitude, longitude, addr.latitude, addr.longitude) <= distance_km
    ]

    return nearby_addresses


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c