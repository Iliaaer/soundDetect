# soundDetect

whisper - https://github.com/openai/whisper

pyannote-audio - https://github.com/pyannote/pyannote-audio

Сервер: FastAPI
База данных:  PostgeSQL
Кэш: redis
Очередь задачь: Celery
Распознование голоса: whisper
Деление на динамики: pyannote-audio

Установка:
```bash
conda create -n rec python=3.9
conda activate rec

pip install chardet sqlalchemy[asyncio] numpy alembic asyncpg fastapi[all] fastapi-users[sqlalchemy] python-dotenv  aiofiles fastapi-cache2[redis] celery flower python-multipart
pip install git+https://github.com/openai/whisper.git 
pip install -qq https://github.com/pyannote/pyannote-audio/archive/refs/tags/2.1.1.zip
```

Создание базы данных:
```bash
alembic revision --autogenerate -m "Database creation"
alembic upgrade head
```

Запуск всего:
```bash
celery -A src.tasks.tasks:celery worker --loglevel=INFO --pool=solo
celery -A src.tasks.tasks:celery flower
uvicorn src.main:app --reload
```
