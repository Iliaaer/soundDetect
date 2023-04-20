from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Распознование голоса"
)


@app.get("/")
def get_hello():
    return "Hello world!"

fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trade", "name": "Matt"},
    {"id": 4, "role": "trade", "name": "Matt", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]}
]

class DegreeType(Enum):
    newbi = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []

@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


face_trades = [
    {"id": 1, "user_id": 1, "price": 122},
    {"id": 2, "user_id": 1, "price": 100}
]


class Trade(BaseModel):
    id: int
    user_id: int
    price: float = Field(ge=0)

@app.post("/trades")
def post_add_trades(trades: List[Trade]):
    face_trades.extend(trades)
    return {"status": 200, "data": face_trades}






