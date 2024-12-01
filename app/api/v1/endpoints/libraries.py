from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.library import Library
from app.schemas.library import LibraryCreate, Library as LibrarySchema
from fastapi_versioning import version


router = APIRouter()

@router.post("/", response_model=LibrarySchema)
@version(1)
async def create_library(
    *,
    db: Session = Depends(get_db),
    library_in: LibraryCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new library (admin only)"""
    library = Library(**library_in.model_dump())
    db.add(library)
    db.commit()
    db.refresh(library)
    return library

@router.get("/", response_model=List[LibrarySchema])
@version(1)
async def get_libraries(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all libraries"""
    libraries = db.query(Library).offset(skip).limit(limit).all()
    return libraries

@router.get("/{library_id}", response_model=LibrarySchema)
@version(1)
async def get_library(
    library_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get library by ID"""
    library = db.query(Library).filter(Library.id == library_id).first()
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    return library

@router.put("/{library_id}", response_model=LibrarySchema)
@version(1)
async def update_library(
    library_id: int,
    library_in: LibraryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update library (admin only)"""
    library = db.query(Library).filter(Library.id == library_id).first()
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    
    for field, value in library_in.model_dump().items():
        setattr(library, field, value)
    
    db.commit()
    db.refresh(library)
    return library 