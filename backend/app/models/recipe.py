from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON

class Food(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    name: str
    local_name: str
    calories: int
    protein: int
    carbohydrates: int
    fat: int
    fiber: int
    glycemic_index: str
    calorie_density: str
    recommended_portion: str
    health_benefits: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    ingredients: List[Dict[str, str]] = Field(default_factory=list, sa_column=Column(JSON))
    origin: str
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    difficulty: str


class Combination(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    local_name: str
    components: List[str] = Field(sa_column=Column(JSON))
    total_calories: int
    total_protein: int
    total_carbohydrates: int
    total_fat: int
    total_fiber: int
    glycemic_index: str
    health_highlights: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    meal_type: str
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    difficulty: str