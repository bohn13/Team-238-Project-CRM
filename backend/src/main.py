from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from routes import accounts_router
from routes import patients_router
settings = get_settings()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_tags=[
        {
            "name": "accounts",
            "description": "Authentication, account lifecycle and user roles.",
        },
    ],
)

app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(patients_router, prefix="/api")

origins = [settings.FRONTEND_BASE_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health/", tags=["health"])
async def health_check():
    return {"status": "ok"}
