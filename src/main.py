from fastapi import FastAPI

from src.audiofiles.router import router as router_audiofile


app = FastAPI(
    title="Sound Detect"
)

app.include_router(router_audiofile) 


# @app.get("/hello")
# async def get_hello():
#     return "Hello world!"

# @app.post("/auth")
# async def auth_acc(username: str, password: str):
#     return {"Result": "OK", "username": username, "password": password}





