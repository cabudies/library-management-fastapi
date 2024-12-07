from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PublicationFrequencyEnum(str, Enum):
    WEEKLY = "weekly"
    FORTNIGHTLY = "fortnightly"
    MONTHLY = "monthly"

class PuzzleDifficultyEnum(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

# Book Schemas
class BookBase(BaseModel):
    title: str
    publisher_id: int

class BookCreate(BookBase):
    pass

class BookEditionBase(BaseModel):
    book_id: Optional[int] = 0
    edition_number: str
    publication_year: int
    author_ids: List[int]

class BookEditionCreate(BookEditionBase):
    pass

class BookEdition(BookEditionBase):
    id: int
    
    class Config:
        from_attributes = True

class Book(BookBase):
    id: int
    editions: List[BookEdition]
    
    class Config:
        from_attributes = True

# Magazine Schemas
class MagazineBase(BaseModel):
    title: str
    publisher_id: int
    frequency: PublicationFrequencyEnum

class MagazineCreate(MagazineBase):
    pass

class MagazineVolumeBase(BaseModel):
    magazine_id: Optional[int] = None
    year: int
    volume_number: int

class MagazineVolumeCreate(MagazineVolumeBase):
    pass

class MagazineVolume(MagazineVolumeBase):
    id: int
    
    class Config:
        from_attributes = True

class Magazine(MagazineBase):
    id: int
    volumes: List[MagazineVolume]
    
    class Config:
        from_attributes = True

# Puzzle Schemas
class PuzzleBase(BaseModel):
    name: str
    difficulty: PuzzleDifficultyEnum
    pieces_count: int
    manufacturer_id: int

class PuzzleCreate(PuzzleBase):
    pass

class Puzzle(PuzzleBase):
    id: int
    
    class Config:
        from_attributes = True

# Author Schemas
class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    
    class Config:
        from_attributes = True

# Item Copy Schemas
class ItemCopyBase(BaseModel):
    library_id: int
    book_edition_id: Optional[int] = None
    magazine_volume_id: Optional[int] = None
    puzzle_id: Optional[int] = None
    duration_in_days: int

class ItemCopyCreate(ItemCopyBase):
    pass

class ItemCopy(ItemCopyBase):
    id: int
    
    class Config:
        from_attributes = True 