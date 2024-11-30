from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from app.core.config import settings
from app.api.v1.endpoints import checkouts
from app.core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Add routes
app.include_router(
    checkouts.router,
    prefix=f"{settings.API_V1_STR}/checkouts",
    tags=["checkouts"]
)

# Add versioning
app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
    description='Library Management System API'
)
