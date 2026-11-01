from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class Food(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: Optional[str] = Field(default=None, unique=True)
    category: str
    name: str
    local_name: str

    # New cultural / cooking fields
    tribe_subgroup: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    meal_occasion: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    season: Optional[str] = None
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    serving_size: Optional[str] = None

    # Existing nutritional fields (unchanged)
    calories: int = 0
    protein: int = 0
    carbohydrates: int = 0
    fat: int = 0
    fiber: int = 0
    glycemic_index: str = ""
    calorie_density: str = ""
    recommended_portion: str = ""

    # Dietary & allergens
    dietary_flags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    allergens: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    health_benefits: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    # Ingredients & instructions – upgraded structure
    ingredients: List[Dict[str, Optional[str]]] = Field(default_factory=list, sa_column=Column(JSON))
    instructions: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    preparation_steps: List[str] = Field(default_factory=list, sa_column=Column(JSON))

    origin: str = ""
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    difficulty: str = "easy"

    # Media fields
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    image_credit: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_type: Optional[str] = None

    # Workflow fields
    cooking_time: Optional[int] = None          # kept for compatibility
    submitted_by: Optional[str] = None
    status: str = Field(default="approved")
    is_featured: bool = False



class Combination(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)   # str, not int
    slug: Optional[str] = Field(default=None, unique=True)
    name: str
    local_name: str
    components: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    component_ids: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    total_calories: int = 0
    total_protein: int = 0
    total_carbohydrates: int = 0
    total_fat: int = 0
    total_fiber: int = 0
    glycemic_index: str = ""
    health_highlights: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    meal_type: str = ""
    meal_occasion: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    difficulty: str = "easy"
    serving_order: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    serving_tips: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    total_cook_time_minutes: Optional[int] = None
    steps: List[dict] = Field(default_factory=list, sa_column=Column(JSON))