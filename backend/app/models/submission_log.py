from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class SubmissionLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="food.id", ondelete="CASCADE")
    old_status: Optional[str] = None
    new_status: str
    performed_by: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))