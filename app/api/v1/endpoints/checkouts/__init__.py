from fastapi import APIRouter
from app.api.v1.endpoints.checkouts import issue, returns, history

router = APIRouter()

# Include all checkout-related routers
router.include_router(issue.router, prefix="", tags=["checkouts"])
router.include_router(returns.router, prefix="/return", tags=["checkouts"])
router.include_router(history.router, prefix="/history", tags=["checkouts"]) 