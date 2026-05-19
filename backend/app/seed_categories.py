from sqlmodel import Session, select
from app.database import engine
from app.models.recipe import Food
from app.models.category import Category

def seed_categories():
    with Session(engine) as session:
        foods = session.exec(select(Food)).all()
        existing_names = {c.name for c in session.exec(select(Category)).all()}
        new_cats = set()
        for food in foods:
            if food.category and food.category not in existing_names:
                new_cats.add(food.category)
        for name in new_cats:
            session.add(Category(name=name))
        if new_cats:
            session.commit()