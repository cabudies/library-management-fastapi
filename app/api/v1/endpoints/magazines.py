from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi_versioning import version

from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.item import Magazine, MagazineVolume
from app.schemas.item import (
    MagazineCreate, Magazine as MagazineSchema,
    MagazineVolumeCreate, MagazineVolume as MagazineVolumeSchema
)

router = APIRouter()

@router.post("/", response_model=MagazineSchema)
@version(1)
async def create_magazine(
    *,
    db: Session = Depends(get_db),
    magazine_in: MagazineCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new magazine (admin only)"""
    magazine = Magazine(**magazine_in.model_dump())
    db.add(magazine)
    db.commit()
    db.refresh(magazine)
    return magazine

@router.get("/", response_model=List[MagazineSchema])
@version(1)
async def get_magazines(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all magazines"""
    magazines = db.query(Magazine).offset(skip).limit(limit).all()
    return magazines

@router.get("/{magazine_id}", response_model=MagazineSchema)
@version(1)
async def get_magazine(
    magazine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get magazine by ID"""
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    return magazine

@router.put("/{magazine_id}", response_model=MagazineSchema)
@version(1)
async def update_magazine(
    magazine_id: int,
    magazine_in: MagazineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update magazine (admin only)"""
    magazine = db.query(Magazine).filter(Magazine.id == magazine_id).first()
    if not magazine:
        raise HTTPException(status_code=404, detail="Magazine not found")
    
    for field, value in magazine_in.model_dump().items():
        setattr(magazine, field, value)
    
    db.commit()
    db.refresh(magazine)
    return magazine

@router.post("/volumes", response_model=MagazineVolumeSchema)
@version(1)
async def create_magazine_volume(
    *,
    db: Session = Depends(get_db),
    volume_in: MagazineVolumeCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new magazine volume (admin only)"""
    volume = MagazineVolume(**volume_in.model_dump())
    db.add(volume)
    db.commit()
    db.refresh(volume)
    return volume 