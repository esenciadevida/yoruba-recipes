from sqlmodel import Session
from app.models.recipe import Food

def create_recipe(db: Session, recipe: Food) -> Food:
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def update_recipe(db: Session, recipe_id: int, updates: dict) -> Food:
    recipe = db.get(Food, recipe_id)
    if not recipe:
        raise ValueError("Recipe not found")
    for key, value in updates.items():
        setattr(recipe, key, value)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe_id: int):
    recipe = db.get(Food, recipe_id)
    if recipe:
        db.delete(recipe)
        db.commit()

def approve_recipe(db: Session, recipe_id: int) -> Food:
    return update_recipe(db, recipe_id, {"status": "approved"})

def reject_recipe(db: Session, recipe_id: int):
    recipe = db.get(Food, recipe_id)
    if recipe:
        recipe.status = "rejected"
        db.commit()

def feature_recipe(db: Session, recipe_id: int, featured: bool) -> Food:
    return update_recipe(db, recipe_id, {"is_featured": featured})