import logging

from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.db.db import init_db, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


@app.on_event("startup")
def init():
    with Session(engine) as db:
        logger.info("Creating initial data")
        init_db(db=db)
        logger.info("Initial data created")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_V1_STR)
