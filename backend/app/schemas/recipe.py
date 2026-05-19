from typing import Optional, List, Dict
from pydantic import BaseModel

# ---------- Food ----------
class FoodBase(BaseModel):
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
    health_benefits: List[str]
    ingredients: List[Dict[str, str]]
    origin: str
    tags: List[str]
    difficulty: str

class FoodCreate(FoodBase):
    pass

class FoodUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    local_name: Optional[str] = None
    calories: Optional[int] = None
    protein: Optional[int] = None
    carbohydrates: Optional[int] = None
    fat: Optional[int] = None
    fiber: Optional[int] = None
    glycemic_index: Optional[str] = None
    calorie_density: Optional[str] = None
    recommended_portion: Optional[str] = None
    health_benefits: Optional[List[str]] = None
    ingredients: Optional[List[Dict[str, str]]] = None
    origin: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[str] = None

class FoodResponse(FoodBase):
    id: int

# ---------- Combination ----------
class CombinationBase(BaseModel):
    name: str
    local_name: str
    components: List[str]
    total_calories: int
    total_protein: int
    total_carbohydrates: int
    total_fat: int
    total_fiber: int
    glycemic_index: str
    health_highlights: List[str]
    meal_type: str
    tags: List[str]
    difficulty: str

class CombinationCreate(CombinationBase):
    pass

class CombinationResponse(CombinationBase):
    id: int