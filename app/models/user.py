from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    MEMBER = "member"
    ADMIN = "admin"
    MANAGER = "manager"

class Honorific(str, enum.Enum):
    MR = "Mr."
    MRS = "Mrs."
    MS = "Ms."

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # hashed_password = Column(String, nullable=False, default="hashed_password")
    full_name = Column(String)
    honorific = Column(Enum(Honorific), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.MEMBER)
    
    # Relationships
    checkouts = relationship("Checkout", back_populates="user")
