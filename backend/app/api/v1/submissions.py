from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select
from typing import List, Optional
from app.db.session import get_session
from app.models.recipe import Food
from app.models.user import User            # <-- REQUIRED IMPORT
from app.models.submission_log import SubmissionLog
from app.schemas.recipe import FoodSubmit, FoodResponse
from app.api.deps import get_current_user
from app.services.submission_service import log_action

router = APIRouter()


# ── Public submit ──────────────────────────────────────
@router.post("/", response_model=FoodResponse, status_code=201)
def submit_recipe(
    submission: FoodSubmit,
    db: Session = Depends(get_session),
):
    # Check for duplicate recipe name
    existing = db.exec(
        select(Food).where(Food.name == submission.name)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="A recipe with this name already exists.")

    food = Food(**submission.model_dump())
    food.status = "pending"
    db.add(food)
    db.commit()
    db.refresh(food)

    log_action(
        db,
        recipe_id=food.id,
        new_status="pending",
        performed_by=submission.submitted_by or "anonymous",
    )
    return food


# ── Admin: list pending ─────────────────────────────────
@router.get("/pending", response_model=List[FoodResponse])
def list_pending(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_session),
    _: User = Depends(get_current_user),       # now User is defined
):
    statement = select(Food).where(Food.status == "pending").offset(skip).limit(limit)
    return db.exec(statement).all()


# ── Admin: approve ──────────────────────────────────────
@router.put("/{recipe_id}/approve", response_model=FoodResponse)
def approve(
    recipe_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    recipe = db.get(Food, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    old_status = recipe.status
    recipe.status = "approved"
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    log_action(
        db,
        recipe_id=recipe.id,
        old_status=old_status,
        new_status="approved",
        performed_by=current_user.username,
    )
    return recipe


# ── Admin: reject ───────────────────────────────────────
@router.put("/{recipe_id}/reject")
def reject(
    recipe_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    recipe = db.get(Food, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    old_status = recipe.status
    recipe.status = "rejected"
    db.add(recipe)
    db.commit()

    log_action(
        db,
        recipe_id=recipe.id,
        old_status=old_status,
        new_status="rejected",
        performed_by=current_user.username,
    )
    return {"message": "Recipe rejected"}


# ── Admin: delete submission ────────────────────────────
@router.delete("/{recipe_id}", status_code=204)
def delete_submission(
    recipe_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    recipe = db.get(Food, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    old_status = recipe.status

    log_action(
        db,
        recipe_id=recipe.id,
        old_status=old_status,
        new_status="deleted",
        performed_by=current_user.username,
    )
    db.delete(recipe)
    db.commit()
    return Response(status_code=204)


# ── Admin: history ─────────────────────────────────────
@router.get("/history")
def get_submission_history(
    db: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    logs = db.exec(
        select(SubmissionLog).order_by(SubmissionLog.timestamp.desc())
    ).all()
    return [
        {
            "id": log.id,
            "recipe_id": log.recipe_id,
            "old_status": log.old_status,
            "new_status": log.new_status,
            "performed_by": log.performed_by,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]