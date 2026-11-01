from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.db.session import get_session
from app.models.recipe import Food, Combination
from app.models.category import Category
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/")
def get_stats(
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user),
):
    approved = db.exec(
        select(func.count(Food.id)).where(Food.status == "approved")
    ).one()
    pending = db.exec(
        select(func.count(Food.id)).where(Food.status == "pending")
    ).one()
    rejected = db.exec(
        select(func.count(Food.id)).where(Food.status == "rejected")
    ).one()
    categories = db.exec(select(func.count(Category.id))).one()
    combinations = db.exec(select(func.count(Combination.id))).one()

    return {
        "total_recipes": approved,
        "pending_submissions": pending,
        "rejected_count": rejected,
        "total_categories": categories,
        "total_combinations": combinations,
    }