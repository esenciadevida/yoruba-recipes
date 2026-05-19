import json
from sqlmodel import Session, select
from app.database import engine
from app.models.recipe import Food, Combination

def seed_data_if_empty():
    with Session(engine) as session:
        # Check if data already exists
        if session.exec(select(Food)).first() is not None:
            return  # already seeded

        # Load the JSON file
        with open("data/recipes.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Insert foods
        for item in data["foods"]:
            food = Food(
                category=item["category"],
                name=item["name"],
                local_name=item["local_name"],
                calories=item["calories"],
                protein=item["protein"],
                carbohydrates=item["carbohydrates"],
                fat=item["fat"],
                fiber=item["fiber"],
                glycemic_index=item["glycemic_index"],
                calorie_density=item["calorie_density"],
                recommended_portion=item["recommended_portion"],
                health_benefits=item["health_benefits"],
                ingredients=item["ingredients"],
                origin=item["origin"],
                tags=item["tags"],
                difficulty=item["difficulty"],
            )
            session.add(food)

        # Insert combinations
        for item in data["combinations"]:
            comb = Combination(
                name=item["name"],
                local_name=item["local_name"],
                components=item["components"],
                total_calories=item["total_calories"],
                total_protein=item["total_protein"],
                total_carbohydrates=item["total_carbohydrates"],
                total_fat=item["total_fat"],
                total_fiber=item["total_fiber"],
                glycemic_index=item["glycemic_index"],
                health_highlights=item["health_highlights"],
                meal_type=item["meal_type"],
                tags=item["tags"],
                difficulty=item["difficulty"],
            )
            session.add(comb)

        session.commit()