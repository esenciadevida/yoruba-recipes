from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.db.session import get_session
from app.models.recipe import Combination
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

# ---------- Pydantic schemas ----------
class CombinationCreate(BaseModel):
    name: str
    local_name: str
    components: List[str] = []
    component_ids: List[str] = []
    total_calories: int = 0
    total_protein: int = 0
    total_carbohydrates: int = 0
    total_fat: int = 0
    total_fiber: int = 0
    glycemic_index: str = ""
    health_highlights: List[str] = []
    meal_type: str = ""
    meal_occasion: List[str] = []
    tags: List[str] = []
    difficulty: str = "easy"
    serving_order: List[str] = []
    serving_tips: List[str] = []
    total_cook_time_minutes: Optional[int] = None
    steps: List[dict] = []

class CombinationUpdate(BaseModel):
    name: Optional[str] = None
    local_name: Optional[str] = None
    components: Optional[List[str]] = None
    component_ids: Optional[List[str]] = None
    total_calories: Optional[int] = None
    total_protein: Optional[int] = None
    total_carbohydrates: Optional[int] = None
    total_fat: Optional[int] = None
    total_fiber: Optional[int] = None
    glycemic_index: Optional[str] = None
    health_highlights: Optional[List[str]] = None
    meal_type: Optional[str] = None
    meal_occasion: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[str] = None
    serving_order: Optional[List[str]] = None
    serving_tips: Optional[List[str]] = None
    total_cook_time_minutes: Optional[int] = None
    steps: Optional[List[dict]] = None

# ---------- Public endpoints ----------
@router.get("/", response_model=List[dict])
def list_combinations(
    search: Optional[str] = Query(None),
    meal_type: Optional[str] = Query(None),
    tag: Optional[str] = Query(None, description="Filter by a specific taxonomy tag"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Combination)
    
    # Text search on fields
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Combination.name.ilike(pattern), Combination.local_name.ilike(pattern))
        )
        
    # Standard string filtering
    if meal_type:
        statement = statement.where(Combination.meal_type == meal_type)
        
    # Taxonomy array/JSON filtering 
    if tag:
        # Works perfectly if tags are stored as a JSON/JSONB array or string array
        statement = statement.where(Combination.tags.contains(tag))

    # Pagination
    statement = statement.offset(skip).limit(limit)
    results = session.exec(statement).all()

    # Automatically serializes objects to your response_model structure
    return [c.dict() for c in results]

@router.get("/{combo_id}")
def get_combination(combo_id: int, session: Session = Depends(get_session)):
    combo = session.get(Combination, combo_id)
    if not combo:
        raise HTTPException(status_code=404, detail="Combination not found")
    return combo

# ---------- Admin endpoints ----------
@router.post("/", response_model=dict, status_code=201)
def create_combination(
    combo: CombinationCreate,
    session: Session = Depends(get_session),
    _: None = Depends(get_current_user),
):
    new = Combination(**combo.dict())
    session.add(new)
    session.commit()
    session.refresh(new)
    return new

@router.put("/{combo_id}")
def update_combination(
    combo_id: int,
    updates: CombinationUpdate,
    session: Session = Depends(get_session),
    _: None = Depends(get_current_user),
):
    combo = session.get(Combination, combo_id)
    if not combo:
        raise HTTPException(status_code=404, detail="Combination not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(combo, key, value)
    session.add(combo)
    session.commit()
    session.refresh(combo)
    return combo

@router.delete("/{combo_id}", status_code=204)
def delete_combination(
    combo_id: int,
    session: Session = Depends(get_session),
    _: None = Depends(get_current_user),
):
    combo = session.get(Combination, combo_id)
    if not combo:
        raise HTTPException(status_code=404, detail="Combination not found")
    session.delete(combo)
    session.commit()
    return {}