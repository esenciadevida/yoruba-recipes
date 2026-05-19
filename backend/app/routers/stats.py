from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.recipe import Food, Combination
from app.models.category import Category
from app.auth import get_current_user

router = APIRouter(prefix="/api/stats", tags=["Stats"])

@router.get("/")
def get_stats(session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    food_count = session.exec(select(func.count(Food.id))).one()
    cat_count = session.exec(select(func.count(Category.id))).one()
    return {
        "total_recipes": food_count,
        "total_categories": cat_count,
    }