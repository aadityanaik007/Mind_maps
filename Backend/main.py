from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.news_controller import router as news_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router)