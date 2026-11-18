from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.public.v1.router import router as public_v1_router
from app.api.private.v1.router import router as private_v1_router
from app.db.init_db import init_db
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(
    title="Payment Platform API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^(https://([a-z0-9-]+\.)?roominary\.com|http://([a-z0-9-]+\.)?localhost:\d+)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_v1_router)
app.include_router(private_v1_router)
