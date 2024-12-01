from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.core.database import get_db
from app.models.user import User
from app.models.item import Puzzle
from app.schemas.item import PuzzleCreate, Puzzle as PuzzleSchema

router = APIRouter()

@router.post("/", response_model=PuzzleSchema)
async def create_puzzle(
    *,
    db: Session = Depends(get_db),
    puzzle_in: PuzzleCreate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Create new puzzle (admin only)"""
    puzzle = Puzzle(**puzzle_in.model_dump())
    db.add(puzzle)
    db.commit()
    db.refresh(puzzle)
    return puzzle

@router.get("/", response_model=List[PuzzleSchema])
async def get_puzzles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get all puzzles"""
    puzzles = db.query(Puzzle).offset(skip).limit(limit).all()
    return puzzles

@router.get("/{puzzle_id}", response_model=PuzzleSchema)
async def get_puzzle(
    puzzle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_member)
):
    """Get puzzle by ID"""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    return puzzle

@router.put("/{puzzle_id}", response_model=PuzzleSchema)
async def update_puzzle(
    puzzle_id: int,
    puzzle_in: PuzzleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """Update puzzle (admin only)"""
    puzzle = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    for field, value in puzzle_in.model_dump().items():
        setattr(puzzle, field, value)
    
    db.commit()
    db.refresh(puzzle)
    return puzzle 