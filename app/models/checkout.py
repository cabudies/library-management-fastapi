from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Checkout(Base):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_copy_id = Column(Integer, ForeignKey("item_copies.id"))
    checkout_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="checkouts")
    item_copy = relationship("ItemCopy", back_populates="checkouts")
