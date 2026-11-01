from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.site_config import SiteConfig
from app.schemas.site_config import SiteConfigUpdate
from app.api.deps import get_current_user

router = APIRouter(prefix="/site-config", tags=["Site Configuration"])

# GET public config (no auth required for footer/legal pages)
@router.get("/")
def get_config(db: Session = Depends(get_session)):
    config = db.exec(select(SiteConfig)).first()
    if not config:
        # Create default config if missing
        config = SiteConfig()
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

# Admin update (requires authentication)
@router.put("/", response_model=SiteConfig)
def update_config(
    update: SiteConfigUpdate,
    db: Session = Depends(get_session),
    _: None = Depends(get_current_user),
):
    config = db.exec(select(SiteConfig)).first()
    if not config:
        config = SiteConfig()
        db.add(config)
    update_data = update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(config, key, value)
    db.commit()
    db.refresh(config)
    return config