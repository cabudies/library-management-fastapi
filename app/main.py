from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from app.core.config import settings
from app.api.v1.endpoints import checkouts


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Add routes
app.include_router(
    checkouts.router,
    prefix=f"/checkouts",
    tags=["checkouts"]
)

# Add versioning
app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/library-management-system/v{major}',
    description='Library Management System API'
)
