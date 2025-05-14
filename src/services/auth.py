import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.schemas.user import User, UserLogin
from src.config import settings


class AuthService:

    # Инициализация контекста хэширования паролей
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    
    # Создание токена доступа
    def create_access_token(sefl, data: dict) -> str:
        """
        Создает токен доступа на основе предоставленных данных.

        Args:
            data (dict): Данные, которые будут закодированы в токен.

        Returns:
            str: Сгенерированный токен доступа.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    # Хеширование пароля
    def hash_password(self, password: str) -> str:
        """
        Хеширует пароль с использованием алгоритма bcrypt.

        Args:
            password (str): Пароль для хеширования.

        Returns:
            str: Хешированный пароль.
        """
        return self.pwd_context.hash(password)
    
    # Проверка пароля
    def __verify_password__(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    # Аутентификация пользователя
    async def login_user(self, session, user: UserLogin) -> User:
        """
        Аутентификация пользователя.

        Args:
            session: Сессия базы данных.
            user (UserLogin): Объект пользователя для аутентификации.

        Returns:
            User: Объект пользователя.

        Raises:
            HTTPException: Если аутентификация не удалась.
        """
        user: User = await UsersRepository(session).auth_user(user, self.__verify_password__)
        return user