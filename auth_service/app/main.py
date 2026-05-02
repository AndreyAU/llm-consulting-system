from fastapi import FastAPI
from app.core.config import settings


app = FastAPI()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
    }
