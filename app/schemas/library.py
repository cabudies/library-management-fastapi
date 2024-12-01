from pydantic import BaseModel
from typing import List

class LibraryBase(BaseModel):
    name: str
    address: str

class LibraryCreate(LibraryBase):
    pass

class Library(LibraryBase):
    id: int
    
    class Config:
        from_attributes = True

class PublisherBase(BaseModel):
    name: str

class PublisherCreate(PublisherBase):
    pass

class Publisher(PublisherBase):
    id: int
    
    class Config:
        from_attributes = True

class ManufacturerBase(BaseModel):
    name: str

class ManufacturerCreate(ManufacturerBase):
    pass

class Manufacturer(ManufacturerBase):
    id: int
    
    class Config:
        from_attributes = True 