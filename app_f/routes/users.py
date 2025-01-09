from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from app_f.models.user import NewUser, UserSignIn, UserDB
from app_f.data_base.connection import get_session

user_router = APIRouter(
    tags=["User"]
)

users = {}

from passlib.context import CryptContext

# Инициализация контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@user_router.post("/signup")
async def sign_new_user(data: NewUser, session: Session = Depends(get_session)) -> dict:
    # Проверяем, существует ли пользователь с таким login
    user_exists = session.query(UserDB).filter(UserDB.login == data.login).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )

    # Хэшируем пароль перед сохранением
    hashed_password = pwd_context.hash(data.password)

    # Создаем нового пользователя с хэшированным паролем
    new_user = UserDB(
        telegram=data.telegram,
        login=data.login,
        password=hashed_password,  # Сохраняем хэшированный пароль
        photo=data.photo,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "User successfully registered!"
    }


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn, session: Session = Depends(get_session)):
    '''
    Проверка пользователя и вход в систему
    :param user: Данные пользователя для входа
    :return: Сообщение об успешном входе или ошибка
    '''
    # Ищем пользователя по логину
    user_exists = session.query(UserDB).filter(UserDB.login == user.login).first()

    # Проверяем, существует ли пользователь с таким логином
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # Проверяем, совпадает ли пароль
    if not pwd_context.verify(user.password, user_exists.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )

    return {
        "message": "User signed in successfully",
        "login": user_exists.login
    }