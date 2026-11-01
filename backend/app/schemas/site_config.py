from pydantic import BaseModel
from typing import Optional

class SiteConfigUpdate(BaseModel):
    contact_email: Optional[str] = None
    instagram_url: Optional[str] = None
    twitter_url: Optional[str] = None
    facebook_url: Optional[str] = None