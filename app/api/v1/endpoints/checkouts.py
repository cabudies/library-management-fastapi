from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.checkout import Checkout
from app.models.item import ItemCopy
from app.schemas.checkout import CheckoutCreate, Checkout as CheckoutSchema
from datetime import datetime

router = APIRouter()

@router.post("/checkout", response_model=CheckoutSchema)
async def checkout_item(
    *,
    db: Session = Depends(get_db),
    checkout_in: CheckoutCreate,
    current_user: User = Depends(deps.get_current_active_member)
):
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

@router.post("/return/{checkout_id}")
async def return_item(
    checkout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    checkout = db.query(Checkout).filter(Checkout.id == checkout_id).first()
    if not checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checkout not found"
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

@router.get("/history/item/{item_copy_id}", response_model=List[CheckoutSchema])
async def get_item_checkout_history(
    item_copy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    checkouts = db.query(Checkout).filter(
        Checkout.item_copy_id == item_copy_id
    ).all()
    return checkouts

@router.get("/history/my", response_model=List[CheckoutSchema])
async def get_my_checkout_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    checkouts = db.query(Checkout).filter(
        Checkout.user_id == current_user.id
    ).all()
    return checkouts 