from fastapi import APIRouter
from app.api.v1 import newsletter
from app.api.v1 import recipes, categories, auth, stats, submissions, site_config
from app.api.v1 import recipes
from app.api.v1 import combinations
from app.api.v1 import developer
router = APIRouter()

router.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
router.include_router(categories.router, prefix="/categories", tags=["Categories"])
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(stats.router, prefix="/stats", tags=["Stats"])
router.include_router(submissions.router, prefix="/admin/submissions", tags=["Admin Submissions"])
router.include_router(site_config.router, tags=["Site Configuration"])
router.include_router(newsletter.router, prefix="/newsletter", tags=["Newsletter"])
router.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
router.include_router(combinations.router, prefix="/combinations", tags=["Combinations"])
router.include_router(developer.router, prefix="/developer", tags=["Developer API"])