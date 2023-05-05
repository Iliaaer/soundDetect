# soundDetect

whisper - https://github.com/openai/whisper

pyannote-audio - https://github.com/pyannote/pyannote-audio

```bash
conda create -n pyannote python=3.8
conda activate pyannote

conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch

pip install -qq https://github.com/pyannote/pyannote-audio/archive/develop.zip

pip install git+https://github.com/openai/whisper.git 
```

Fast API

```bash
pip install fastapi[all]
pip install fastapi-users[sqlalchemy]
pip install asyncpg
pip install python-multipart
```

Создание базы данных:

```bash
alembic revision --autogenerate -m "Database creation"
alembic upgrade head
```

База данных:  PostgeSQL

```bash
pip install sqlalchemy alembic psycopg2
alembic init migrations
```

Кэш: redis

Очередь задачь: Celery

Запуск всего:

```bash
celery -A src.tasks.tasks:celery worker --loglevel=INFO --pool=solo
celery -A src.tasks.tasks:celery flower
uvicorn src.main:app --reload
```
