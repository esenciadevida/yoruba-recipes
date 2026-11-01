from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_session),
):
    return db.exec(select(Category)).all()


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user)
):
    # Check for duplicate name
    existing = db.exec(select(Category).where(Category.name == cat_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(**cat_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{cat_id}", response_model=CategoryResponse)
def update_category(
    cat_id: int,
    cat_in: CategoryUpdate,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user)
):
    category = db.get(Category, cat_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in cat_in.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{cat_id}", status_code=204)
def delete_category(
    cat_id: int,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user)
):
    category = db.get(Category, cat_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return Response(status_code=204)