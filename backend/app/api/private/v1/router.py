from fastapi import APIRouter
from app.api.private.v1 import health, shift_applications
from app.api.private.v1 import shifts
from app.api.private.v1 import employer_shifts
from app.api.private.v1 import employers
from app.api.private.v1 import businesses
from app.api.private.v1 import workers
from app.api.private.v1 import session
from app.api.private.v1 import skills

router = APIRouter(prefix="/api/private/v1")

router.include_router(workers.router)
router.include_router(session.router)
router.include_router(businesses.router)
router.include_router(employers.router)
router.include_router(employer_shifts.router)
router.include_router(shifts.router)
router.include_router(skills.router)
router.include_router(health.router)
router.include_router(shift_applications.router)
