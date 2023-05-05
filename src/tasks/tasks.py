from celery import Celery
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session, async_sessionmaker
import asyncio
from sqlalchemy.ext.declarative import declarative_base
from asyncio import current_task
from contextlib import asynccontextmanager
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from src.audiofiles.models import audiofile
# from src.pyannote_whisper.utils import diarize_text
from src.config import PIPELINE_TOKEN

import whisper
from pyannote.audio import Pipeline
from pyannote.core import notebook
from pyannote.audio import Audio

audio = Audio(sample_rate=16000, mono=True)

DEVICE_WHISPER = 'cpu'
MODEL_WHISPER  = 'large'

celery = Celery('tasks', broker='redis://localhost:6379') # задаем подключение к планировшику Celery

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}' # задаем подключение к бд postgresql
Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False) # делаем сессию к бд ансихроной

loop = asyncio.get_event_loop()

pipeline = Pipeline.from_pretrained( # создаем подключение к pyannote.audio
    'pyannote/speaker-diarization@2.1', 
    use_auth_token=PIPELINE_TOKEN
)

model = whisper.load_model( # создаем подключение к whisper
    name=MODEL_WHISPER, 
    device=DEVICE_WHISPER
)

print('ALL READY')

@asynccontextmanager
async def scoped_session():
    """
    Функция scoped_session - это функция, которая создает класс сеанса, 
    который можно использовать в качестве асинхронного контекстного менеджера. 
    Сеанс, возвращенный контекстным менеджером, будет закрыт при завершении работы контекстного менеджера, 
    и он также удалит сеанс из реестра сеансов с ограниченной областью действия. 
    Это означает, что если вы используете этот контекстный менеджер в нескольких местах, 
    у каждого из них будет свой собственный уникальный сеанс.

    :return: Контекстный менеджер, который возвращает сеанс
    """
    scoped_factory = async_scoped_session(
        session,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()

async def update_res_db_text(out_file_path: str, result: dict):
    """
    Функция update_res_db_text обновляет результирующий столбец строки в таблице аудиофайлов. 
    Функция принимает два аргумента: out_file_path и result. 
    out_file_path - это строка, представляющая имя аудиофайла, которое используется для идентификации рассматриваемой строки. 
    Результирующий аргумент - это словарь, содержащий информацию о том, сколько слов было правильно транскрибировано.
    
    :param out_file_path: str: Укажите путь к файлу обрабатываемого аудиофайла
    :param result: dict: Обновите столбец результата в базе данных
    :return: Результат инструкции update
    """
    stmt = update(audiofile).where(audiofile.c.name == out_file_path).values(result=result)
    async with scoped_session() as s:
        await s.execute(stmt)
        await s.commit()


@celery.task
def recognition_audio_files(out_file_path: str, LANGUAGE: str = 'ru', NUM_SPEAKERS: int = 2):
    """
    Функция recognition_audio_files принимает путь к аудиофайлу и возвращает распознанный текст из этого аудиофайла.

    :param out_file_path: str: Укажите путь к аудиофайлу
    :param LANGUAGE: str: Укажите язык аудиофайла
    :param NUM_SPEAKERS: int: Задайте количество динамиков в аудиофайле
    """
    diarization_result = pipeline(f'wav/{out_file_path}', num_speakers=NUM_SPEAKERS)
    notebook.reset()
    who_speaks_when = diarization_result.rename_labels({"SPEAKER_00": "Говорящий 1", "SPEAKER_01": "Говорящий 2"})
    result = {}
    for segment, _, speaker in who_speaks_when.itertracks(yield_label=True):
        waveform, sample_rate = audio.crop(f'wav/{out_file_path}', segment)
        text = model.transcribe(waveform.squeeze().numpy(), language=LANGUAGE)["text"]
        time = f"{segment.start:.2f}:{segment.end:.2f}"
        print(f"{time} - {speaker}: {text}")
        result[time] = {speaker: text}

    loop.run_until_complete(update_res_db_text(out_file_path, {"data": result}))


    # print('OKEY1')
    # diarization_result = pipeline(f'wav/{out_file_path}', min_speakers=MIN_SPEAKERS, max_speakers=MAX_SPEAKERS)
    # asr_result = model.transcribe(f'wav/{out_file_path}', language=LANGUAGE, fp16=False)
    # final_result = diarize_text(asr_result, diarization_result)

    # result = {'data': {
        # f'{seg.start:.2f}:{seg.end:.2f}': {spk: sent}
        # for seg, spk, sent in final_result
    # }}
    # result = {'data': 'Загружается'}
    # print('OKEY3')
    # loop.run_until_complete(update_res_db_text(out_file_path, result))
    # print('OKEY4')