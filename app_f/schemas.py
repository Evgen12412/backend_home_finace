from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    telegram: str
    password: str
    db_name: str