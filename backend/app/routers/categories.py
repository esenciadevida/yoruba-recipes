from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.database import get_session
from app.models.category import Category
from app.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/categories", tags=["Categories"])

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None

@router.get("/", response_model=List[dict])
def list_categories(session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    categories = session.exec(select(Category)).all()
    return [{"id": c.id, "name": c.name, "description": c.description, "icon": c.icon} for c in categories]

@router.post("/", response_model=dict, status_code=201)
def create_category(cat_in: CategoryCreate, session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    existing = session.exec(select(Category).where(Category.name == cat_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(**cat_in.dict())
    session.add(category)
    session.commit()
    session.refresh(category)
    return {"id": category.id, "name": category.name, "description": category.description, "icon": category.icon}

@router.put("/{cat_id}", response_model=dict)
def update_category(cat_id: int, cat_in: CategoryUpdate, session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    category = session.get(Category, cat_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if cat_in.name is not None:
        category.name = cat_in.name
    if cat_in.description is not None:
        category.description = cat_in.description
    if cat_in.icon is not None:
        category.icon = cat_in.icon
    session.add(category)
    session.commit()
    session.refresh(category)
    return {"id": category.id, "name": category.name, "description": category.description, "icon": category.icon}

@router.delete("/{cat_id}", status_code=204)
def delete_category(cat_id: int, session: Session = Depends(get_session), _: None = Depends(get_current_user)):
    category = session.get(Category, cat_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()