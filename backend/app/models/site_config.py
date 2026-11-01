from sqlmodel import SQLModel, Field
from typing import Optional

class SiteConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_email: str = "yorubarecipe.org"
    instagram_url: str = ""
    twitter_url: str = ""
    facebook_url: str = ""