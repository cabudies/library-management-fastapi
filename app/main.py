from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from app.core.config import settings
from app.api.v1.endpoints import (
    auth, users, books, magazines, puzzles,
    libraries, publishers, manufacturers, checkouts
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Add routes
app.include_router(
    auth.router,
    prefix=f"/auth",
    tags=["auth"]
)

app.include_router(
    users.router,
    prefix=f"/users",
    tags=["users"]
)

app.include_router(
    libraries.router,
    prefix=f"/libraries",
    tags=["libraries"]
)

app.include_router(
    publishers.router,
    prefix=f"/publishers",
    tags=["publishers"]
)

app.include_router(
    manufacturers.router,
    prefix=f"/manufacturers",
    tags=["manufacturers"]
)

app.include_router(
    books.router,
    prefix=f"/books",
    tags=["books"]
)

app.include_router(
    magazines.router,
    prefix=f"/magazines",
    tags=["magazines"]
)

app.include_router(
    puzzles.router,
    prefix=f"/puzzles",
    tags=["puzzles"]
)

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
