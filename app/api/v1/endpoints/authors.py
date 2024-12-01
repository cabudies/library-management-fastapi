from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.item import Author
from app.schemas.item import AuthorCreate, Author as AuthorSchema
from fastapi_versioning import version

router = APIRouter()

@router.post("/", response_model=AuthorSchema)
@version(1)
async def create_author(
    *,
    db: Session = Depends(get_db),
    author_in: AuthorCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new author (admin only)"""
    author = Author(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

@router.get("/", response_model=List[AuthorSchema])
@version(1)
async def get_authors(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all authors"""
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors

@router.get("/{author_id}", response_model=AuthorSchema)
@version(1)
async def get_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get author by ID"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=AuthorSchema)
@version(1)
async def update_author(
    author_id: int,
    author_in: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update author (admin only)"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for field, value in author_in.model_dump().items():
        setattr(author, field, value)
    
    db.commit()
    db.refresh(author)
    return author 