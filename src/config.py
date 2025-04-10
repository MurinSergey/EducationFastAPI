from pydantic_settings import BaseSettings, SettingsConfigDict

# Класс настроек приложения
# Настройки загружаются из файла .env и преобразуются в объект класса Settings
class Settings(BaseSettings):
    DB_HOST: str  # Хост базы данных
    DB_PORT: int  # Порт базы данных
    DB_USER: str  # Пользователь базы данных
    DB_PASS: str  # Пароль пользователя базы данных
    DB_NAME: str  # Название базы данных

    # Свойство, которое возвращает строку подключения к базе данных
    @property # Декоратор @property позволяет обращаться к этому методу как к атрибуту класса
    def DATABASE_URL(self) -> str:
        # Форматирование строки подключения к базе данных
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    # Настройки для загрузки настроек из файла .env и его кодировкой
    model_config = SettingsConfigDict(env_file='.env')

# Создаем объект настроек и загружаем их из файла .env
settings = Settings()