# English Cards Bot🤖
Бот для изучения английских слов с помощью интерактивных карточек.

---

## 🚀 Основные функции
- 📚 **Тренировка слов** из стандартной коллекции (цвета) и пользовательских карточек.
- 🗃️ **Управление карточками**: добавление своих слов, удаление ненужных.
- 🔄 **Сброс прогресса**: восстановление начальной коллекции.
- ✅ **Валидация**: проверка ввода на корректность (русский/английский алфавит).
- 📖 **Пагинация**: удобный просмотр коллекции с кнопками "Вперед/Назад".

---

## ⚙️ Технологии
- **Python 3.10+**
- **Aiogram 3.x**
- **SQLAlchemy 2.0**

---

## 🛠️ Установка и запуск

**Предварительные требования:**
- Установленный Python 3.10+
- Сервер PostgreSQL

1. **Создайте файл `.env` на основе `.env.example`**:

```ini
BOT_TOKEN=ваш_токен_бота
DB_URL=postgresql+asyncpg://user:password@localhost/dbname
```

2. **Установите зависимости**:

```bash
pip install -r requirements.txt
```

3. **Запустите бота**:

```bash
python main.py
```

---

## 🗄️ База данных

Бот автоматически создает таблицы при первом запуске по схеме:

![Схема БД](./database/scheme.png)

**Таблицы:**
- `users` — данные пользователей
- `user_words` — пользовательские слова
- `default_words` — слова по умолчанию
- `user_ignored_words` — слова по умолчанию скрытые для пользователя

---

## 🖥️ Пример работы

1. Начало работы `/start`:

![Пример работы команды /start](./images_work/start.png)

2. Список команд `/help`:

![Пример работы команды /help](./images_work/help.png)

3. Меню с командами:

![Пример работы кнопки menu](./images_work/menu.png)

4. Просмотр доступных карточек `/cards`:

![Пример работы команды /cards](./images_work/cards.png)

5. Добавить новую карточку `/addcard`:

![Пример работы команды /addcard](./images_work/addcard.png)

6. Отменить пользовательские изменения по команде `/reset`:

![Пример работы команды /reset](./images_work/reset.png)

7. Начало тренировки `/beginning`:

![Пример работы команды /beginning](./images_work/beginning.png)

8. Процесс тренировки:

![Пример тренировки](./images_work/training.png)