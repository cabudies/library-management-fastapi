from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.library import Publisher
from app.schemas.library import PublisherCreate, Publisher as PublisherSchema

router = APIRouter()

@router.post("/", response_model=PublisherSchema)
async def create_publisher(
    *,
    db: Session = Depends(get_db),
    publisher_in: PublisherCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new publisher (admin only)"""
    publisher = Publisher(**publisher_in.model_dump())
    db.add(publisher)
    db.commit()
    db.refresh(publisher)
    return publisher

@router.get("/", response_model=List[PublisherSchema])
async def get_publishers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all publishers"""
    publishers = db.query(Publisher).offset(skip).limit(limit).all()
    return publishers

@router.get("/{publisher_id}", response_model=PublisherSchema)
async def get_publisher(
    publisher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get publisher by ID"""
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

@router.put("/{publisher_id}", response_model=PublisherSchema)
async def update_publisher(
    publisher_id: int,
    publisher_in: PublisherCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update publisher (admin only)"""
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    
    for field, value in publisher_in.model_dump().items():
        setattr(publisher, field, value)
    
    db.commit()
    db.refresh(publisher)
    return publisher 