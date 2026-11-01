from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.db.session import get_session
from app.models.recipe import Food
from app.models.api_key import ApiKey
from app.core.rate_limit import limiter

router = APIRouter()

# ── Helper: optional API key verification ──
async def verify_api_key(
    api_key: Optional[str] = None,
    db: Session = Depends(get_session)
) -> Optional[str]:
    if api_key:
        key_obj = db.exec(select(ApiKey).where(ApiKey.key == api_key)).first()
        if not key_obj or not key_obj.active:
            raise HTTPException(status_code=403, detail="Invalid API key")
        return api_key
    return None

# ── Public endpoints ──
@router.get("/recipes")
@limiter.limit("30/minute")
def developer_recipes(
    request: Request,
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    region: Optional[str] = Query(None, alias="origin"),
    featured: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=50),
    db: Session = Depends(get_session),
    api_key: Optional[str] = Depends(verify_api_key),
):
    statement = select(Food).where(Food.status == "approved")
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Food.name.ilike(pattern), Food.local_name.ilike(pattern))
        )
    if category:
        statement = statement.where(Food.category == category)
    if difficulty:
        statement = statement.where(Food.difficulty == difficulty)
    if region:
        statement = statement.where(Food.origin == region)
    if featured is not None:
        statement = statement.where(Food.is_featured == featured)
    statement = statement.offset(skip).limit(limit)
    return db.exec(statement).all()


@router.get("/recipes/{slug_or_id}")
@limiter.limit("30/minute")
def developer_recipe_detail(
    request: Request,   # ← Added this parameter
    slug_or_id: str,
    db: Session = Depends(get_session),
):
    recipe = None
    if slug_or_id.isdigit():
        recipe = db.get(Food, int(slug_or_id))
    if not recipe:
        recipe = db.exec(select(Food).where(Food.slug == slug_or_id)).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/regions")
@limiter.limit("30/minute")
def developer_regions(request: Request, db: Session = Depends(get_session)):   # ← Added request
    origins = db.exec(select(Food.origin).distinct()).all()
    return [o[0] for o in origins if o[0]]


@router.get("/tags")
@limiter.limit("30/minute")
def developer_tags(request: Request, db: Session = Depends(get_session)):   # ← Added request
    foods = db.exec(select(Food.tags)).all()
    tags = set()
    for ftags in foods:
        if ftags:
            tags.update(ftags)
    return sorted(list(tags))


@router.get("/ingredients")
@limiter.limit("30/minute")
def developer_ingredients(request: Request, db: Session = Depends(get_session)):   # ← Added request
    foods = db.exec(select(Food.ingredients)).all()
    ingredient_names = set()
    for ing_list in foods:
        if ing_list:
            for ing in ing_list:
                if isinstance(ing, dict):
                    ingredient_names.add(ing.get("name", ""))
    return sorted([i for i in ingredient_names if i])


@router.get("/categories")
@limiter.limit("30/minute")
def developer_categories(request: Request, db: Session = Depends(get_session)):   # ← Added request
    cats = db.exec(select(Food.category).distinct()).all()
    return [c[0] for c in cats if c[0]]