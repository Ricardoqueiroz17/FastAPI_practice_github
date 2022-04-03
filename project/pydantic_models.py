from pydantic import BaseModel
from typing import List

class User(BaseModel):
    username: str
    password: str
    likes: List[str]