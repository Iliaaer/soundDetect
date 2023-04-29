from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.audiofiles.router import router as router_audiofile


app = FastAPI(
    title="Sound Detect"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_audiofile) 

