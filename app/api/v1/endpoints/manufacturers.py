from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.library import Manufacturer
from app.schemas.library import ManufacturerCreate, Manufacturer as ManufacturerSchema
from fastapi_versioning import version


router = APIRouter()

@router.post("/", response_model=ManufacturerSchema)
@version(1)
async def create_manufacturer(
    *,
    db: Session = Depends(get_db),
    manufacturer_in: ManufacturerCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new manufacturer (admin only)"""
    manufacturer = Manufacturer(**manufacturer_in.model_dump())
    db.add(manufacturer)
    db.commit()
    db.refresh(manufacturer)
    return manufacturer

@router.get("/", response_model=List[ManufacturerSchema])
@version(1)
async def get_manufacturers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all manufacturers"""
    manufacturers = db.query(Manufacturer).offset(skip).limit(limit).all()
    return manufacturers

@router.get("/{manufacturer_id}", response_model=ManufacturerSchema)
@version(1)
async def get_manufacturer(
    manufacturer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get manufacturer by ID"""
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer

@router.put("/{manufacturer_id}", response_model=ManufacturerSchema)
@version(1)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer_in: ManufacturerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update manufacturer (admin only)"""
    manufacturer = db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    
    for field, value in manufacturer_in.model_dump().items():
        setattr(manufacturer, field, value)
    
    db.commit()
    db.refresh(manufacturer)
    return manufacturer 