from typing import Optional, List, Dict
from pydantic import BaseModel

class Ingredient(BaseModel):
    name: str
    local_name: Optional[str] = None
    quantity: str
    substitution: Optional[str] = None

class FoodBase(BaseModel):
    slug: Optional[str] = None
    category: str
    name: str
    local_name: str
    tribe_subgroup: List[str] = []
    meal_occasion: List[str] = []
    season: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    serving_size: Optional[str] = None
    calories: int = 0
    protein: int = 0
    carbohydrates: int = 0
    fat: int = 0
    fiber: int = 0
    glycemic_index: str = ""
    calorie_density: str = ""
    recommended_portion: str = ""
    dietary_flags: List[str] = []
    allergens: List[str] = []
    health_benefits: List[str] = []
    ingredients: List[Ingredient] = []
    instructions: List[str] = []
    origin: str = ""
    tags: List[str] = []
    difficulty: str = "easy"
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    image_credit: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_type: Optional[str] = None

class FoodCreate(FoodBase):
    pass

class FoodUpdate(BaseModel):
    # All fields optional for partial updates
    slug: Optional[str] = None
    category: Optional[str] = None
    name: Optional[str] = None
    local_name: Optional[str] = None
    tribe_subgroup: Optional[List[str]] = None
    meal_occasion: Optional[List[str]] = None
    season: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    serving_size: Optional[str] = None
    calories: Optional[int] = None
    protein: Optional[int] = None
    carbohydrates: Optional[int] = None
    fat: Optional[int] = None
    fiber: Optional[int] = None
    glycemic_index: Optional[str] = None
    calorie_density: Optional[str] = None
    recommended_portion: Optional[str] = None
    dietary_flags: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    health_benefits: Optional[List[str]] = None
    ingredients: Optional[List[Ingredient]] = None
    instructions: Optional[List[str]] = None
    origin: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    image_credit: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_type: Optional[str] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None

class FoodSubmit(BaseModel):
    """Used for public submissions – fewer required fields."""
    name: str
    local_name: str
    category: str
    difficulty: str = "easy"
    cooking_time: Optional[int] = None
    origin: Optional[str] = None
    submitted_by: Optional[str] = None
    image_url: Optional[str] = None
    ingredients: List[Ingredient] = []
    instructions: List[str] = []
    preparation_steps: List[str] = []
    health_benefits: List[str] = []
    tags: List[str] = []
    calories: int = 0
    protein: int = 0
    carbohydrates: int = 0
    fat: int = 0
    fiber: int = 0
    glycemic_index: str = ""
    calorie_density: str = ""
    recommended_portion: str = ""
class FoodResponse(FoodBase):
    id: int
    status: str = "approved"
    submitted_by: Optional[str] = None
    is_featured: bool = False
    cooking_time: Optional[int] = None   # legacy