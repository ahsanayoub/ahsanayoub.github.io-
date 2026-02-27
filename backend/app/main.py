from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.requisitions import router as requisitions_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(requisitions_router)
