from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select, func
from typing import List, Optional
from app.database import get_session
from app.models.recipe import Food
from app.schemas.recipe import FoodCreate, FoodUpdate, FoodResponse
from app.auth import get_current_user
from app.services import food_service

router = APIRouter(prefix="/api/foods", tags=["Foods"])

@router.get("/", response_model=List[FoodResponse])
def list_foods(
    response: Response,
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    session: Session = Depends(get_session),
):
    # Base query
    statement = select(Food)
    count_statement = select(func.count(Food.id))
    
    # Filters
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            Food.name.ilike(pattern) | Food.local_name.ilike(pattern)
        )
        count_statement = count_statement.where(
            Food.name.ilike(pattern) | Food.local_name.ilike(pattern)
        )
    if category:
        statement = statement.where(Food.category == category)
        count_statement = count_statement.where(Food.category == category)
    if difficulty:
        statement = statement.where(Food.difficulty == difficulty)
        count_statement = count_statement.where(Food.difficulty == difficulty)
    if tag:
        # Filtering JSON arrays is tricky; we'll filter in Python for simplicity
        pass

    # Get total count
    total = session.exec(count_statement).one()
    response.headers["X-Total-Count"] = str(total)

    # Apply pagination
    statement = statement.offset(skip).limit(limit)
    results = session.exec(statement).all()

    # Optional tag filtering in Python (if tag parameter provided)
    if tag:
        results = [f for f in results if tag in f.tags]

    return results

@router.post("/", response_model=FoodResponse, status_code=201)
def create_food(food_in: FoodCreate, session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    food = Food(**food_in.model_dump())
    return food_service.create_food(session, food)

@router.get("/{food_id}", response_model=FoodResponse)
def get_food(
    food_id: int,
    session: Session = Depends(get_session),
):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food

@router.put("/{food_id}", response_model=FoodResponse)
def update_food(food_id: int, food_update: FoodUpdate, session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    updated = food_service.update_food(session, food_id, food_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Food not found")
    return updated

@router.delete("/{food_id}", status_code=204)
def delete_food(food_id: int, session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    deleted = food_service.delete_food(session, food_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Food not found")