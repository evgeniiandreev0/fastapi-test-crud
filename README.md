# Система управления задачами

Это API для управления персональными задачами с аутентификацией пользователей, построенное на FastAPI, PostgreSQL и Redis.

## Содержание

1. [Установка и запуск](#установка-и-запуск)
2. [Аутентификация](#аутентификация)
3. [Управление задачами](#управление-задачами)
4. [API Reference](#api-reference)
5. [Разработка](#разработка)

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Git

### Шаги установки

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Создайте файл `.env` с переменными окружения:
   ```
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/task_manager
   REDIS_URL=redis://redis:6379/0
   SECRET_KEY=replace_with_more_secure_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Запустите приложение с помощью Docker Compose:
   ```bash
   docker compose up -d
   ```

4. Приложение будет доступно по адресу: http://localhost:8512

## Аутентификация

### Создание пользователя

1. Откройте Swagger UI: http://localhost:8512/docs
2. Найдите эндпоинт `POST /users/` и кликните "Try it out"
3. Введите данные нового пользователя:
   ```json
   {
     "username": "your_username",
     "email": "your_email@example.com",
     "password": "your_password"
   }
   ```
4. Нажмите "Execute"

### Получение токена

1. Найдите эндпоинт `POST /users/token` и кликните "Try it out"
2. Введите данные авторизации:
   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```
3. Нажмите "Execute"
4. Скопируйте полученный `access_token`

### Авторизация через Swagger UI

1. Нажмите на кнопку "Authorize" в правом верхнем углу
2. В открывшемся окне введите:
   - Username: ваш_логин
   - Password: ваш_пароль
   - Остальные поля оставьте пустыми
3. Нажмите "Authorize" и затем "Close"
4. Теперь вы авторизованы для выполнения защищенных запросов

## Управление задачами

### Создание задачи

```bash
curl -X POST "http://localhost:8512/tasks/" \
-H "Authorization: Bearer ваш_access_token" \
-H "Content-Type: application/json" \
-d '{
"title": "Название задачи",
"description": "Описание задачи",
"status": "в ожидании",
"priority": 1
}'
```

### Получение списка задач

```bash
curl -X GET "http://localhost:8512/tasks/" \
-H "Authorization: Bearer ваш_access_token"
```

### Получение задачи по ID

```bash
curl -X GET "http://localhost:8512/tasks/1" \
-H "Authorization: Bearer ваш_access_token"
```

### Обновление задачи

```bash
url -X PUT "http://localhost:8512/tasks/1" \
-H "Authorization: Bearer ваш_access_token" \
-H "Content-Type: application/json" \
-d '{
"title": "Обновленное название",
"description": "Обновленное описание",
"status": "в работе",
"priority": 2
}'
```

### Удаление задачи

```bash
curl -X DELETE "http://localhost:8512/tasks/1" \
-H "Authorization: Bearer ваш_access_token"
```

## API Reference

### Пользователи

- `POST /users/` - Создание нового пользователя
- `POST /users/token` - Получение токена авторизации
- `GET /users/me` - Получение информации о текущем пользователе

### Задачи

- `GET /tasks/` - Получение списка задач с поддержкой сортировки и пагинации
- `POST /tasks/` - Создание новой задачи
- `GET /tasks/{task_id}` - Получение задачи по ID
- `PUT /tasks/{task_id}` - Обновление задачи
- `DELETE /tasks/{task_id}` - Удаление задачи
- `GET /tasks/priority/top` - Получение задач с наивысшим приоритетом
- `GET /tasks/search/` - Поиск задач по ключевому слову

## Разработка

### Миграции

Для создания новой миграции:
```bash
docker compose exec web uv run alembic revision --autogenerate -m "description"
```
