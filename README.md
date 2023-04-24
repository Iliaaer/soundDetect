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

tets.py

```bash
pip install pytorch_lightning==1.6 torch-audiomentations==0.11.0 asteroid-filterbanks==0.4 pyannote.metrics==3.2 pyannote.pipeline==2.3 speechbrain torchaudio==2.0.0 torch==2.0.0 hmmlearn==0.2.6
pip install pyannote.audio --no-deps
```



Фротенд: ??? Нужен ли?

Беэкнд:

API: Fast API или Flask

Fast API

```bash
pip install fastapi[all]
pip install fastapi-users[sqlalchemy]
pip install asyncpg
pip install python-multipart

```

run:

```bash
uvicorn main:app --reload
```

создание базы данных:

```bash
alembic revision --autogenerate -m "Database creation"
alembic upgrade head

```

База данных: mysql или PostgeSQL

postgeSQL

```bash
pip install sqlalchemy alembic psycopg2
alembic init migrations
```

Текстовый поиск: elasticsearch

Хранение файлов: ???

Кэш: redis или memcached  -  Нужен ли?

Очередь задачь: Celery или RabbitMQ - Нужен ли?

Нейроные сети: самописное на паралельном потоке...

Сбор логов: grayLog, logstash

Визуализация логов: kibana
