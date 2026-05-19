from typing import List, Optional
from sqlmodel import Session, select, or_
from app.models.recipe import Food, Combination
from app.models.category import Category

# ---------- Food CRUD ----------
def _sync_category(session: Session, category_name: Optional[str]):
    if not category_name:
        return
    existing = session.exec(select(Category).where(Category.name == category_name)).first()
    if not existing:
        session.add(Category(name=category_name))
        session.commit()

def create_food(session: Session, food: Food) -> Food:
    session.add(food)
    session.commit()
    session.refresh(food)
    _sync_category(session, food.category)
    return food

def get_foods(
    session: Session,
    search: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    tag: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Food]:
    statement = select(Food)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Food.name.ilike(pattern), Food.local_name.ilike(pattern))
        )
    if category:
        statement = statement.where(Food.category == category)
    if difficulty:
        statement = statement.where(Food.difficulty == difficulty)
    if tag:
        # tag filtering: check if tag is in the JSON array
        # SQLite: use json_each or LIKE; for portability we can filter in Python after query
        # For simplicity here we return all and filter in Python (ok for small dataset)
        pass
    statement = statement.offset(skip).limit(limit)
    results = session.exec(statement).all()
    if tag:
        results = [f for f in results if tag in f.tags]
    return results

def get_food(session: Session, food_id: int) -> Optional[Food]:
    return session.get(Food, food_id)

def update_food(session: Session, food_id: int, update_data: dict) -> Optional[Food]:
    food = session.get(Food, food_id)
    if not food:
        return None
    for key, value in update_data.items():
        if value is not None:
            setattr(food, key, value)
    session.add(food)
    session.commit()
    session.refresh(food)
    _sync_category(session, food.category)
    return food

def delete_food(session: Session, food_id: int) -> bool:
    food = session.get(Food, food_id)
    if not food:
        return False
    session.delete(food)
    session.commit()
    return True

# ---------- Combination (read mostly) ----------
def get_combinations(session: Session, skip: int = 0, limit: int = 100) -> List[Combination]:
    statement = select(Combination).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_combination(session: Session, comb_id: int) -> Optional[Combination]:
    return session.get(Combination, comb_id)