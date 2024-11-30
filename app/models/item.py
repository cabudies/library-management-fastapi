from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class PublicationFrequency(str, enum.Enum):
    WEEKLY = "weekly"
    FORTNIGHTLY = "fortnightly"
    MONTHLY = "monthly"

class PuzzleDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

# Association table for book editions and authors
edition_authors = Table(
    'edition_authors',
    Base.metadata,
    Column('edition_id', Integer, ForeignKey('book_editions.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    
    # Relationships
    editions = relationship("BookEdition", secondary=edition_authors, back_populates="authors")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    
    # Relationships
    publisher = relationship("Publisher", back_populates="books")
    editions = relationship("BookEdition", back_populates="book")

class BookEdition(Base):
    __tablename__ = "book_editions"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    edition_number = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=False)
    
    # Relationships
    book = relationship("Book", back_populates="editions")
    authors = relationship("Author", secondary=edition_authors, back_populates="editions")
    copies = relationship("ItemCopy", back_populates="book_edition")

class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
    frequency = Column(Enum(PublicationFrequency), nullable=False)
    
    # Relationships
    publisher = relationship("Publisher", back_populates="magazines")
    volumes = relationship("MagazineVolume", back_populates="magazine")

class MagazineVolume(Base):
    __tablename__ = "magazine_volumes"

    id = Column(Integer, primary_key=True, index=True)
    magazine_id = Column(Integer, ForeignKey("magazines.id"))
    year = Column(Integer, nullable=False)
    volume_number = Column(Integer, nullable=False)
    
    # Relationships
    magazine = relationship("Magazine", back_populates="volumes")
    copies = relationship("ItemCopy", back_populates="magazine_volume")

class Puzzle(Base):
    __tablename__ = "puzzles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    difficulty = Column(Enum(PuzzleDifficulty), nullable=False)
    pieces_count = Column(Integer, nullable=False)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    
    # Relationships
    manufacturer = relationship("Manufacturer", back_populates="puzzles")
    copies = relationship("ItemCopy", back_populates="puzzle")

class ItemCopy(Base):
    __tablename__ = "item_copies"

    id = Column(Integer, primary_key=True, index=True)
    library_id = Column(Integer, ForeignKey("libraries.id"))
    book_edition_id = Column(Integer, ForeignKey("book_editions.id"), nullable=True)
    magazine_volume_id = Column(Integer, ForeignKey("magazine_volumes.id"), nullable=True)
    puzzle_id = Column(Integer, ForeignKey("puzzles.id"), nullable=True)
    
    # Relationships
    library = relationship("Library", back_populates="item_copies")
    book_edition = relationship("BookEdition", back_populates="copies")
    magazine_volume = relationship("MagazineVolume", back_populates="copies")
    puzzle = relationship("Puzzle", back_populates="copies")
    checkouts = relationship("Checkout", back_populates="item_copy")
