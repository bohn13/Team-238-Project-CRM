from routes.accounts import router as accounts_router
from routes.doctors import router as doctors_router
from routes.patients import router as patients_router

__all__ = ["accounts_router", "doctors_router", "patients_router"]
