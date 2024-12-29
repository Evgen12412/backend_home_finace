from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlmodel import SQLModel, Field



class User(BaseModel):
    '''
    Модель User будет использоваться в качестве модели ответа, когда мы не хотим взаимодействовать с паролем
    '''
    telegram:str
    login:str
    password: str
    photo: Optional[str] = None


    class Config:
        json_schema_extra = {
            "example": {
                "login": "exmp",
                "password": "strong!!!",
                "photo": "_"
            }
        }

class NewUser(User):
    telegram: str
    login: str
    password: str


class UserSignIn(BaseModel):
    '''
    модель для входа пользователей
    '''
    login: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "login": "exampl",
                "password": "strong!!!",
            }
        }

class UserDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram: str
    login: str
    password: str
    photo: Optional[str] = None