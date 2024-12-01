from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.checkout import Checkout

router = APIRouter()

@router.post("/{checkout_id}")
async def return_item(
    checkout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Return a checked out item"""
    checkout = db.query(Checkout).filter(Checkout.id == checkout_id).first()
    if not checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No checkout record was found for the given ID"
        )
    
    if checkout.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to return this item"
        )
    
    if checkout.return_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already returned"
        )
    
    checkout.return_date = datetime.utcnow()
    db.commit()
    db.refresh(checkout)
    return {"message": "Item returned successfully"} 