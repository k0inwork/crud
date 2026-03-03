import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (чтобы пароли не торчали в коде)
load_dotenv()

class Config:
    # Настройка базы данных. Если переменная DATABASE_URL не задана, будем использовать sqlite для тестов (на всякий случай)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///diary.db'

    # Отключаем предупреждения SQLAlchemy о том, что что-то там меняется, чтобы не засорять консоль
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Секретный ключ нужен для безопасности, например, чтобы формы работали (CSRF и т.д.)
    # Если его нет в .env, то ставим дефолтный (но лучше всегда задавать свой!)
    SECRET_KEY = os.getenv('SECRET_KEY') or 'my-super-secret-key-for-my-diary'
