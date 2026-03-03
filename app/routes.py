from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import db, Entry

# Создаем блюпринт (это как бы кусочек нашего приложения, чтобы все не писать в одном файле)
main_bp = Blueprint('main', __name__)

# Главная страница - тут мы будем видеть все наши записи (список)
# Она отвечает на запросы GET (просто посмотреть) и POST (если форма что-то отправила)
@main_bp.route('/', methods=['GET'])
def index():
    try:
        # Достаем все записи из базы (начинаем с новых, поэтому order_by)
        entries = Entry.query.order_by(Entry.created_at.desc()).all()

        # Если в URL есть параметр ?json=1 или ?json=true, то возвращаем JSON
        if request.args.get('json'):
            # Проходимся по всем записям и делаем из них словари с помощью to_dict()
            entries_list = [entry.to_dict() for entry in entries]
            return jsonify({'entries': entries_list, 'status': 'success'})

        # Если параметра нет, то просто рисуем HTML страничку (шаблон index.html)
        # Передаем туда наши записи, чтобы шаблон смог их показать
        return render_template('index.html', entries=entries)

    except Exception as e:
        # Если что-то пошло не так (например, база упала), мы ловим ошибку тут
        # Возвращаем простой JSON с ошибкой
        return jsonify({'error': str(e), 'message': 'Упс, что-то пошло не так на главной странице :('}), 500

# Создание новой записи (CREATE)
@main_bp.route('/create', methods=['GET', 'POST'])
def create_entry():
    try:
        # Если запрос POST, значит пользователь нажал "Сохранить" в форме или прислал JSON
        if request.method == 'POST':
            # Если прислали JSON (через Postman или другой скрипт)
            if request.is_json:
                data = request.get_json()
                # Берем данные из JSON. Если чего-то нет, подставляем пустую строку
                title = data.get('title', '')
                content = data.get('content', '')
            else:
                # А если это обычная HTML форма
                title = request.form.get('title', '')
                content = request.form.get('content', '')

            # Проверяем, чтобы заголовок не был пустым
            if not title:
                return jsonify({'error': 'Название не может быть пустым!'}), 400

            # Создаем новый объект записи с этими данными
            new_entry = Entry(title=title, content=content)

            # Добавляем его в базу данных
            db.session.add(new_entry)

            # И обязательно делаем коммит, иначе ничего не сохранится!
            db.session.commit()

            # Если просили JSON в параметрах или отправляли JSON
            if request.args.get('json') or request.is_json:
                return jsonify({'message': 'Ура, запись создана!', 'entry': new_entry.to_dict()}), 201

            # Если обычный браузер, то редиректим (отправляем) обратно на главную страницу
            return redirect(url_for('main.index'))

        # Если метод GET, то просто показываем формочку для создания (шаблон create.html)
        return render_template('create.html')

    except Exception as e:
        # Обрабатываем непредвиденные ошибки
        return jsonify({'error': str(e), 'message': 'Не удалось создать запись.'}), 500


# Чтение одной конкретной записи (READ)
@main_bp.route('/entry/<int:id>', methods=['GET'])
def get_entry(id):
    try:
        # Ищем запись по ID. Если не найдет - вернет 404 (Not Found)
        # Это магия SQLAlchemy (get_or_404)
        entry = Entry.query.get_or_404(id)

        # Если просят JSON
        if request.args.get('json'):
            return jsonify({'entry': entry.to_dict(), 'status': 'success'})

        # А иначе отдаем шаблон и саму запись туда
        return render_template('view.html', entry=entry)

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Запись не найдена или ошибка БД.'}), 404


# Редактирование записи (UPDATE)
@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    try:
        # Опять ищем нашу запись в БД
        entry = Entry.query.get_or_404(id)

        # Если мы сохраняем изменения (POST)
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                entry.title = data.get('title', entry.title) # Если title нет в JSON, оставляем старый (entry.title)
                entry.content = data.get('content', entry.content)
                # Если передали is_completed в JSON, то обновляем
                if 'is_completed' in data:
                    entry.is_completed = bool(data.get('is_completed'))
            else:
                # Из HTML формы получаем данные (у формы тоже могут быть свои причуды)
                entry.title = request.form.get('title', entry.title)
                entry.content = request.form.get('content', entry.content)
                # Чекбокс в HTML форме: если он нажат, форма шлет 'on', иначе ничего не шлет (None)
                entry.is_completed = request.form.get('is_completed') == 'on'

            # Сохраняем (коммитим) в базу
            db.session.commit()

            if request.args.get('json') or request.is_json:
                return jsonify({'message': 'Запись успешно обновлена!', 'entry': entry.to_dict()})

            # Возвращаемся на главную
            return redirect(url_for('main.index'))

        # Если GET запрос, то показываем формочку с уже заполненными старыми данными
        return render_template('edit.html', entry=entry)

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Ошибка при редактировании.'}), 500


# Удаление записи (DELETE)
# Я использую GET или POST для формы, потому что HTML формы не умеют делать DELETE напрямую, только через JS.
# Но если это API, мы поддерживаем DELETE.
@main_bp.route('/delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_entry(id):
    try:
        # Находим запись, которую будем удалять
        entry = Entry.query.get_or_404(id)

        # Удаляем объект из сессии базы данных
        db.session.delete(entry)

        # Коммитим (сохраняем изменения, то есть окончательно удаляем)
        db.session.commit()

        if request.args.get('json') or request.method == 'DELETE':
            return jsonify({'message': 'Запись удалена навсегда!', 'deleted_id': id})

        # Возвращаем юзера на главную страницу после удаления
        return redirect(url_for('main.index'))

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Не вышло удалить :('}), 500


# Дополнительный маршрут, чтобы быстро менять статус (выполнено / не выполнено)
# Джуны часто делают такие маленькие функции для удобства.
@main_bp.route('/toggle/<int:id>', methods=['GET', 'POST'])
def toggle_completed(id):
    try:
        entry = Entry.query.get_or_404(id)

        # Меняем значение на противоположное (если было True, станет False, и наоборот)
        entry.is_completed = not entry.is_completed

        db.session.commit()

        if request.args.get('json'):
            return jsonify({'message': 'Статус изменен', 'entry': entry.to_dict()})

        return redirect(url_for('main.index'))

    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Ошибка при изменении статуса.'}), 500
