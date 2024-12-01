from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.checkout import Checkout
from app.models.item import ItemCopy
from app.schemas.checkout import CheckoutCreate, Checkout as CheckoutSchema

router = APIRouter()

@router.post("/", response_model=CheckoutSchema)
async def checkout_item(
    *,
    db: Session = Depends(get_db),
    checkout_in: CheckoutCreate,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Issue an item to a member"""
    # Check if item copy exists and is available
    item_copy = db.query(ItemCopy).filter(ItemCopy.id == checkout_in.item_copy_id).first()
    if not item_copy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item copy not found"
        )
    
    # Check if item is already checked out
    active_checkout = db.query(Checkout).filter(
        Checkout.item_copy_id == checkout_in.item_copy_id,
        Checkout.return_date.is_(None)
    ).first()
    
    if active_checkout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item is already checked out"
        )
    
    # Create new checkout
    checkout = Checkout(
        user_id=current_user.id,
        item_copy_id=checkout_in.item_copy_id
    )
    db.add(checkout)
    db.commit()
    db.refresh(checkout)
    return checkout 