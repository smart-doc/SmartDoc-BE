from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.hospitals import router as hospitals_router
from .endpoints.doctors import router as doctors_router
from .endpoints.patients import router as patients_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(hospitals_router, prefix="/hospitals", tags=["Hospitals"])
api_router.include_router(doctors_router, prefix="/doctors", tags=["Doctors"])
api_router.include_router(patients_router, prefix="/patients", tags=["Patients"])