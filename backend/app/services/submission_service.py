from typing import Optional
from sqlmodel import Session
from app.models.submission_log import SubmissionLog

def log_action(
    db: Session,
    recipe_id: int,
    new_status: str,
    performed_by: str,
    old_status: Optional[str] = None,
):
    entry = SubmissionLog(
        recipe_id=recipe_id,
        old_status=old_status,
        new_status=new_status,
        performed_by=performed_by,
    )
    db.add(entry)
    db.commit()