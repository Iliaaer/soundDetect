# soundDetect

whisper - https://github.com/openai/whisper

pyannote-audio - https://github.com/pyannote/pyannote-audio

'''bash
conda create -n pyannote python=3.8
conda activate pyannote

conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch

pip install -qq https://github.com/pyannote/pyannote-audio/archive/develop.zip

pip install git+https://github.com/openai/whisper.git 
'''

Фротенд: ??? Нужен ли?

Беэкнд:

API: Fast API или Flask

База данных: mysql или PostgeSQL

Текстовый поиск: elasticsearch

Хранение файлов: ???

Кэш: redis или memcached  -  Нужен ли?

Очередь задачь: Celery или RabbitMQ - Нужен ли?

Нейроные сети: самописное на паралельном потоке...

Сбор логов: grayLog, logstash

Визуализация логов: kibana
