from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.schemas.recipe import CombinationResponse
from app.services import food_service

router = APIRouter(prefix="/api/combinations", tags=["Combinations"])

@router.get("/", response_model=List[CombinationResponse])
def list_combinations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=200),
    session: Session = Depends(get_session)
):
    return food_service.get_combinations(session, skip, limit)

@router.get("/{comb_id}", response_model=CombinationResponse)
def get_combination(comb_id: int, session: Session = Depends(get_session)):
    comb = food_service.get_combination(session, comb_id)
    if not comb:
        raise HTTPException(status_code=404, detail="Combination not found")
    return comb