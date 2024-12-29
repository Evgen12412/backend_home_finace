from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from app_f.models.user import NewUser, UserSignIn, UserDB
from app_f.data_base.connection import get_session

user_router = APIRouter(
    tags=["User"]
)

users = {}

@user_router.post("/signup")
async def sign_new_user(data: NewUser, session: Session = Depends(get_session)) -> dict:
    # Проверяем, существует ли пользователь с таким login
    user_exists = session.query(UserDB).filter(UserDB.login == data.login).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User with supplied username exists")

    # Создаем нового пользователя
    new_user = UserDB(telegram=data.telegram, login=data.login, password=data.password, photo=data.photo)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "User successfully registered!"
    }


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn):
    '''
    проверка пользователя
    :param user:
    :return:
    '''
    # Проверяем, существует ли пользователь с таким login
    if user.login not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # Получаем пароль из словаря
    stored_password = users[user.login]

    # Сравниваем пароли
    if stored_password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )

    return {
        "message": "User signed in successfully"
    }