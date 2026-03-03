from flask import Flask
from config import Config
from .models import db
from .routes import main_bp

# Функция, которая собирает (инициализирует) наше Flask-приложение
# Джуны любят делать так (Application Factory), потому что так пишут в крутых туториалах
def create_app():
    # Создаем саму программу Flask
    app = Flask(__name__)

    # Говорим ей взять настройки из файла config.py
    app.config.from_object(Config)

    # Привязываем базу данных (Алхимию) к нашему приложению
    db.init_app(app)

    # Прицепляем все наши пути (роуты) из файла routes.py
    # Заметь, мы их берем из Blueprint, который назвали main_bp
    app.register_blueprint(main_bp)

    # Запускаем создание таблиц в базе данных, если их еще нет.
    # Это нужно чтобы SQLAlchemy сама создала табличку entries в PostgreSQL или SQLite
    with app.app_context():
        # Сначала db.create_all() посмотрит все модели (у нас это Entry)
        db.create_all()
        # Если таблица есть, ничего страшного не произойдет (ошибки не будет)

    # Возвращаем готовое приложение, чтобы его можно было запустить
    return app
