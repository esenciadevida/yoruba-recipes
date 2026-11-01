from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select, func, or_
from typing import List, Optional
from app.db.session import get_session
from app.models.recipe import Food
from app.schemas.recipe import FoodCreate, FoodUpdate, FoodResponse
from app.api.deps import get_current_user
from app.services.recipe_service import create_recipe, update_recipe, delete_recipe

router = APIRouter()

@router.get("/", response_model=List[FoodResponse])
def list_recipes(
    response: Response,
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_session),
):
    # Base queries for Food
    statement = select(Food)
    count_statement = select(func.count(Food.id))

    # Apply filters
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Food.name.ilike(pattern), Food.local_name.ilike(pattern))
        )
        count_statement = count_statement.where(
            or_(Food.name.ilike(pattern), Food.local_name.ilike(pattern))
        )
    if category:
        statement = statement.where(Food.category == category)
        count_statement = count_statement.where(Food.category == category)
    if difficulty:
        statement = statement.where(Food.difficulty == difficulty)
        count_statement = count_statement.where(Food.difficulty == difficulty)
    if status:
        statement = statement.where(Food.status == status)
        count_statement = count_statement.where(Food.status == status)
    if featured is not None:
        statement = statement.where(Food.is_featured == featured)
        count_statement = count_statement.where(Food.is_featured == featured)

    # Publicly show only approved recipes
    if status is None:
        statement = statement.where(Food.status == "approved")
        count_statement = count_statement.where(Food.status == "approved")

    # Total count for pagination
    total = db.exec(count_statement).one()
    response.headers["X-Total-Count"] = str(total)

    # Pagination
    statement = statement.offset(skip).limit(limit)
    return db.exec(statement).all()


@router.post("/", response_model=FoodResponse, status_code=201)
def create_food(
    food_in: FoodCreate,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user)
):
    food = Food(**food_in.model_dump())
    return create_recipe(db, food)


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(
    food_id: int,
    db: Session = Depends(get_session),
):
    food = db.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return food


@router.put("/{food_id}", response_model=FoodResponse)
def update_food(
    food_id: int,
    food_update: FoodUpdate,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user)
):
    try:
        return update_recipe(db, food_id, food_update.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{food_id}", status_code=204)
def delete_food(
    food_id: int,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user)
):
    delete_recipe(db, food_id)
    return Response(status_code=204)