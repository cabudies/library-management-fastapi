from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.item import Book, BookEdition, Author
from app.schemas.item import (
    BookCreate, Book as BookSchema,
    BookEditionCreate, BookEdition as BookEditionSchema
)

router = APIRouter()

@router.post("/", response_model=BookSchema)
async def create_book(
    *,
    db: Session = Depends(get_db),
    book_in: BookCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new book (admin only)"""
    book = Book(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/", response_model=List[BookSchema])
async def get_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all books"""
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookSchema)
async def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get book by ID"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    book_in: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update book (admin only)"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for field, value in book_in.model_dump().items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    return book

@router.post("/editions", response_model=BookEditionSchema)
async def create_book_edition(
    *,
    db: Session = Depends(get_db),
    edition_in: BookEditionCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new book edition (admin only)"""
    author_ids = edition_in.author_ids
    edition_data = edition_in.model_dump(exclude={'author_ids'})
    
    edition = BookEdition(**edition_data)
    authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
    edition.authors = authors
    
    db.add(edition)
    db.commit()
    db.refresh(edition)
    return edition 