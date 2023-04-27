from celery import Celery

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio
from sqlalchemy.ext.declarative import declarative_base
from asyncio import current_task
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker
from contextlib import asynccontextmanager
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from src.database import get_async_session
from src.audiofiles.models import audiofile
from src.pyannote_whisper.utils import diarize_text
from src.config import PIPELINE_TOKEN


import whisper
from pyannote.audio import Pipeline


DEVICE_WHISPER = "cpu"
MODEL_WHISPER  = "large"

celery = Celery('tasks', broker='redis://localhost:6379')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)

loop = asyncio.get_event_loop()

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization@2.1", 
    use_auth_token=PIPELINE_TOKEN
)

model = whisper.load_model(
    name=MODEL_WHISPER, 
    device=DEVICE_WHISPER
)

print("ALL READY")

@asynccontextmanager
async def scoped_session():
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
    stmt = update(audiofile).where(audiofile.c.name == out_file_path.split("/")[-1]).values(result=result)
    async with scoped_session() as s:
        await s.execute(stmt)
        await s.commit()


@celery.task
def recognition_audio_files(out_file_path: str, LANGUAGE="ru", MIN_SPEAKERS: int = 1, MAX_SPEAKERS: int = 2,):
    # print("OKEY1")
    diarization_result = pipeline(out_file_path, min_speakers=MIN_SPEAKERS, max_speakers=MAX_SPEAKERS)
    asr_result = model.transcribe(out_file_path, language=LANGUAGE, fp16=False)
    final_result = diarize_text(asr_result, diarization_result)
    # result_all = {}
    # for seg, spk, sent in final_result:
    #     # line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sent}'
    #     result_all[f"{seg.start:.2f}:{seg.end:.2f}"] = {spk: sent}
    # result_all = 
    result = {"data": {
        f"{seg.start:.2f}:{seg.end:.2f}": {spk: sent}
        for seg, spk, sent in final_result
    }}
    # print("OKEY3")
    loop.run_until_complete(update_res_db_text(out_file_path, result))
    # print("OKEY4")

