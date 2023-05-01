from datetime import datetime
from typing import List
import aiofiles
import soundfile as sf
import json

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse

from src.database import get_async_session
from src.audiofiles.models import audiofile
from src.audiofiles.schemas import AudioFileCreate

# from src.tasks.tasks import recognition_audio_files


# import whisper
# from pyannote.audio import Pipeline
# from src.pyannote_whisper.utils import diarize_text
# from src.config import PIPELINE_TOKEN

# pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
#                                     use_auth_token=PIPELINE_TOKEN)
# model = whisper.load_model(name="large", device="cpu")

router = APIRouter(
    prefix="/audiofiles",
    tags=["Audio Files"]
)

@router.get("/allname")
async def get_all_name_audio_file(device_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(audiofile.c.name, audiofile.c.time, audiofile.c.result).where(audiofile.c.device == device_type)
    result = [dict(r._mapping) for r in await session.execute(query)]

    return {"result": 
                [dict({"name": r["name"], "time": r["time"], "already": 0 if r["result"]["data"] == "Загружается" else 1}) for r in result]}

@router.post("/upload")
async def post_audio_file(device_type: str, in_file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    if in_file.filename:
        format_file = in_file.filename.split(".")[-1]
        try:
            assert(format_file == "wav")
        except:
            raise HTTPException(status_code=400, detail={
                "status": "error",
                "filename": None,
                "result": f"Файл формата {format_file} не подерживается. Загрузите аудио файл формата .wav."
            })
    time_now = datetime.utcnow()
    time_now_strftime = time_now.strftime("%d_%m_%Y__%H_%M_%S")
    new_file_name = f"{time_now_strftime}_upload_{in_file.filename}"
    out_file_path = f"wav/{new_file_name}"
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content :=  await in_file.read(1024):
            await out_file.write(content)
    f = sf.SoundFile(out_file_path)
    result_all = {"data": "Загружается"}
    # asr_result = model.transcribe(out_file_path, language="ru", fp16=False)
    # diarization_result = pipeline(out_file_path, min_speakers=MIN_SPEAKERS, max_speakers=MAX_SPEAKERS)
    # final_result = diarize_text(asr_result, diarization_result)
    # result_all = {}
    # for seg, spk, sent in final_result:
    #     line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sent}'
    #     result_all[f"{seg.start:.2f}:{seg.end:.2f}"] = {spk: sent}
    #     print(line)

    # new_audio_file = AudioFileCreate(name=new_file_name, 
    #                                  duration=f'{f.frames/f.samplerate}', 
    #                                  time=time_now, 
    #                                  device=device_type, 
    #                                  result=result_all) 

    # stmt = insert(audiofile).values(**new_audio_file.dict())
    # await session.execute(stmt)
    # await session.commit()
    # recognition_audio_files.delay(out_file_path=out_file_path)
    return {"status": "success", "filename": new_file_name, "result": result_all}

@router.get("/resultfile")
async def get_result_recognition(filename: str, session: AsyncSession = Depends(get_async_session)):
    query = select(audiofile.c.result).where(audiofile.c.name == filename)
    result = await session.execute(query)
    a = [r._mapping for r in result][0]
    return {"result": a["result"]}
    # print(result, type(result))

@router.get("/download")
def get_audio_file(filename: str):
    return FileResponse(f"wav/{filename}")

