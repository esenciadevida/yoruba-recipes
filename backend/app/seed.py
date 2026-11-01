import json
from sqlmodel import Session, select
from app.db.session import engine
from app.models.recipe import Food, Combination

def seed_data_if_empty():
    """
    Seeds the database with foods and combinations from data/recipes.json
    only if the Food table is empty.
    """
    with Session(engine) as session:
        # Check if any food already exists
        if session.exec(select(Food)).first():
            return

        with open("data/recipes.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # ---------- Seed Foods ----------
        for item in data.get("foods", []):
            food = Food(
                # Basic identifiers
                slug=item.get("slug"),
                category=item.get("category", ""),
                name=item.get("name", ""),
                local_name=item.get("local_name", ""),
                
                # Cultural & cooking details
                tribe_subgroup=item.get("tribe_subgroup", []),
                meal_occasion=item.get("meal_occasion", []),
                season=item.get("season"),
                prep_time_minutes=item.get("prep_time_minutes"),
                cook_time_minutes=item.get("cook_time_minutes"),
                serving_size=item.get("serving_size"),
                
                # Nutritional info (legacy fields kept for compatibility)
                calories=item.get("calories", 0),
                protein=item.get("protein", 0),
                carbohydrates=item.get("carbohydrates", 0),
                fat=item.get("fat", 0),
                fiber=item.get("fiber", 0),
                glycemic_index=item.get("glycemic_index", ""),
                calorie_density=item.get("calorie_density", ""),
                recommended_portion=item.get("recommended_portion", ""),
                
                # Dietary & allergens
                dietary_flags=item.get("dietary_flags", []),
                allergens=item.get("allergens", []),
                
                # Health & ingredients
                health_benefits=item.get("health_benefits", []),
                ingredients=item.get("ingredients", []),
                
                # Instructions (new array field, keep old preparation_steps as fallback)
                instructions=item.get("instructions", []),
                preparation_steps=item.get("preparation_steps", []),
                
                origin=item.get("origin", ""),
                tags=item.get("tags", []),
                difficulty=item.get("difficulty", "easy"),
                
                # Media
                image_url=item.get("image_url"),
                video_url=item.get("video_url"),
                image_credit=item.get("image_credit"),
                thumbnail_url=item.get("thumbnail_url"),
                image_type=item.get("image_type"),
                
                # Workflow fields (seeded as approved)
                status="approved",
                submitted_by=None,
                is_featured=False,
                cooking_time=item.get("cooking_time"),  # legacy
            )
            session.add(food)

        # ---------- Seed Combinations ----------
        for item in data.get("combinations", []):
            combo = Combination(
                id=item["id"],                     # string ID from JSON
                slug=item.get("slug"),
                name=item["name"],
                local_name=item.get("local_name", ""),
                components=item.get("components", []),
                component_ids=item.get("component_ids", []),
                total_calories=item.get("total_calories", 0),
                total_protein=item.get("total_protein", 0),
                total_carbohydrates=item.get("total_carbohydrates", 0),
                total_fat=item.get("total_fat", 0),
                total_fiber=item.get("total_fiber", 0),
                glycemic_index=item.get("glycemic_index", ""),
                health_highlights=item.get("health_highlights", []),
                meal_type=item.get("meal_type", ""),
                meal_occasion=item.get("meal_occasion", []),
                tags=item.get("tags", []),
                difficulty=item.get("difficulty", "easy"),
                serving_order=item.get("serving_order", []),
                serving_tips=item.get("serving_tips", []),
                total_cook_time_minutes=item.get("total_cook_time_minutes"),
                steps=item.get("steps", []),
            )
            session.add(combo)

        session.commit()
        print("Database seeded successfully with foods and combinations.")