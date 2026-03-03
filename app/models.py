from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Создаем объект базы данных (пока пустой, привяжем его потом в __init__.py)
db = SQLAlchemy()

# Класс для записей ежедневника (как таблица в SQL)
class Entry(db.Model):
    # Указываем имя таблицы в базе (я люблю называть понятно, entries - это записи)
    __tablename__ = 'entries'

    # Уникальный айдишник для каждой записи (Primary Key - первичный ключ)
    id = db.Column(db.Integer, primary_key=True)

    # Заголовок нашей записи (чтобы было понятно о чем она).
    # Максимум 200 символов, и он не может быть пустым (nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Текст самой записи. Тип Text означает что можно писать сколько угодно символов
    content = db.Column(db.Text, nullable=False)

    # Пометка: выполнена ли задача/запись или нет. По умолчанию False (не выполнена)
    is_completed = db.Column(db.Boolean, default=False)

    # Дата и время создания записи. Заполняется автоматически при создании (datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Функция __repr__ просто помогает нам красиво видеть объекты при отладке в консоли
    def __repr__(self):
        return f'<Entry {self.id} - {self.title}>'

    # Это функция, чтобы легко превращать объект базы в словарик (нужно для API/JSON ответов)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'is_completed': self.is_completed,
            # Превращаем дату в строку чтобы JSON её не боялся
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
