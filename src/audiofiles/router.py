from datetime import datetime
import json
from typing import List
import aiofiles
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import FileResponse

from src.database import get_async_session
from src.audiofiles.models import audiofile
from src.audiofiles.schemas import AudioFileCreate
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder



router = APIRouter(
    prefix="/audiofiles",
    tags=["Audio Files"]
)

@router.get("/allname", response_model=List)
async def get_all_name_audio_file(device_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(audiofile).where(audiofile.c.device == device_type)
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]

@router.post("/upload")
async def post_audio_file(device_type: str, in_file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    time_now = datetime.utcnow()
    time_now_strftime = time_now.strftime("%d_%m_%Y__%H_%M_%S")
    new_file_name = f"{time_now_strftime}_upload_{in_file.filename}"
    out_file_path = f"wav/{new_file_name}"
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content :=  await in_file.read(1024):
            await out_file.write(content)
    new_audio_file = AudioFileCreate(name=new_file_name, time=time_now, device=device_type) 
    stmt = insert(audiofile).values(**new_audio_file.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", "filename": new_file_name}

@router.get("/download")
def get_audio_file(filename: str):
    in_file_path = f"wav/{filename}"
    return FileResponse(in_file_path)