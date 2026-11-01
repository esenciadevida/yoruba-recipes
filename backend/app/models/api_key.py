from sqlmodel import SQLModel, Field
from typing import Optional
import secrets

def generate_key():
    return "yor_" + secrets.token_urlsafe(24)

class ApiKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(default_factory=generate_key, unique=True)
    name: str
    active: bool = True