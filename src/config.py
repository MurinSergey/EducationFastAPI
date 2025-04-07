from pydantic_settings import BaseSettings, SettingsConfigDict

# Класс настроек приложения
# Настройки загружаются из файла .env и преобразуются в объект класса Settings
class Settings(BaseSettings):
    DB_NAME: str # Название базы данных
    DB_PORT: int # Порт базы данных

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8') # Конфигурация загрузки настроек из файла .env

# Создаем объект настроек и загружаем их из файла .env
settings = Settings()