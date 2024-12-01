from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.checkout import Checkout
from app.schemas.checkout import Checkout as CheckoutSchema

router = APIRouter()

@router.get("/item/{item_copy_id}", response_model=List[CheckoutSchema])
async def get_item_checkout_history(
    item_copy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get checkout history for a specific item"""
    checkouts = db.query(Checkout).filter(
        Checkout.item_copy_id == item_copy_id
    ).all()
    return checkouts

@router.get("/my", response_model=List[CheckoutSchema])
async def get_my_checkout_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get current user's checkout history"""
    checkouts = db.query(Checkout).filter(
        Checkout.user_id == current_user.id
    ).all()
    return checkouts 