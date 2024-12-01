from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.item import ItemCopy, BookEdition
from app.schemas.item import ItemCopyCreate, ItemCopy as ItemCopySchema
from fastapi_versioning import version

router = APIRouter()

@router.post("/", response_model=ItemCopySchema)
@version(1)
async def create_item_copy(
    *,
    db: Session = Depends(get_db),
    copy_in: ItemCopyCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new item copy (admin only)"""
    # Validate that only one type of item is specified
    item_types = [
        copy_in.book_edition_id,
        copy_in.magazine_volume_id,
        copy_in.puzzle_id
    ]
    if len([x for x in item_types if x is not None]) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one item type must be specified"
        )
    
    # If it's a book edition, verify it exists
    if copy_in.book_edition_id:
        edition = db.query(BookEdition).filter(
            BookEdition.id == copy_in.book_edition_id
        ).first()
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book edition not found"
            )
    
    copy = ItemCopy(**copy_in.model_dump())
    db.add(copy)
    db.commit()
    db.refresh(copy)
    return copy

@router.get("/", response_model=List[ItemCopySchema])
@version(1)
async def get_item_copies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    library_id: int = None,
    book_edition_id: int = None,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all item copies with optional filters"""
    query = db.query(ItemCopy)
    
    if library_id:
        query = query.filter(ItemCopy.library_id == library_id)
    if book_edition_id:
        query = query.filter(ItemCopy.book_edition_id == book_edition_id)
    
    copies = query.offset(skip).limit(limit).all()
    return copies

@router.get("/{copy_id}", response_model=ItemCopySchema)
@version(1)
async def get_item_copy(
    copy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get item copy by ID"""
    copy = db.query(ItemCopy).filter(ItemCopy.id == copy_id).first()
    if not copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item copy not found"
        )
    return copy

@router.put("/{copy_id}", response_model=ItemCopySchema)
@version(1)
async def update_item_copy(
    copy_id: int,
    copy_in: ItemCopyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update item copy (admin only)"""
    copy = db.query(ItemCopy).filter(ItemCopy.id == copy_id).first()
    if not copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item copy not found"
        )
    
    # Validate that only one type of item is specified
    item_types = [
        copy_in.book_edition_id,
        copy_in.magazine_volume_id,
        copy_in.puzzle_id
    ]
    if len([x for x in item_types if x is not None]) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one item type must be specified"
        )
    
    # If it's a book edition, verify it exists
    if copy_in.book_edition_id:
        edition = db.query(BookEdition).filter(
            BookEdition.id == copy_in.book_edition_id
        ).first()
        if not edition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book edition not found"
            )
    
    for field, value in copy_in.model_dump().items():
        setattr(copy, field, value)
    
    db.commit()
    db.refresh(copy)
    return copy 