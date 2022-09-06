from fastapi import APIRouter

from src.app.routers import create, delete, read, update, webhook

routers = APIRouter()

routers.include_router(create.router)
routers.include_router(delete.router)
routers.include_router(read.router)
routers.include_router(update.router)
routers.include_router(webhook.router)

