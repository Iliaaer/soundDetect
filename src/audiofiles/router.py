from datetime import datetime
import aiofiles
import soundfile as sf

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from fastapi.responses import FileResponse

from src.database import get_async_session
from src.audiofiles.models import audiofile
from src.audiofiles.schemas import AudioFileCreate

# from src.tasks.tasks import recognition_audio_files

router = APIRouter(
    prefix='/audiofiles',
    tags=['Audio Files']
)

@router.get('/allname')
async def get_all_name_audio_file(device_type: str, session: AsyncSession = Depends(get_async_session)):
    """
    Функция get_all_name_audio_file возвращает список всех аудиофайлов в базе данных.
        Функция принимает один параметр, device_type, который используется для фильтрации результатов по типу устройства.
        Функция возвращает объект JSON, содержащий массив объектов с полями name и time.
    
    :параметр device_type: str: Выберите аудиофайлы определенного устройства
    :param session: AsyncSession: Создайте сеанс с базой данных
    :return: Список всех аудиофайлов в базе данных
    """
    query = select(audiofile.c.name, audiofile.c.time, audiofile.c.result).where(audiofile.c.device == device_type)
    result = [dict(r._mapping) for r in await session.execute(query)]
    return {'result': [dict({'name': r['name'], 'time': r['time'], 'data': r['result']['data'],  'already': 0 if r['result']['data'] == 'Загружается' else 1}) for r in result]}

@router.post('/upload')
async def post_audio_file(device_type: str, in_file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    """
    Функция post_audio_file используется для загрузки аудиофайлов.
        Функция принимает следующие параметры:
            device_type (str): тип устройства, на которое был записан аудиофайл.
            in_file (Загрузить файл): Загруженный файл .wav.
    
    :параметр device_type: str: Определяет тип устройства, с которого был загружен аудиофайл
    :параметр in_file: uploadFile: Получить файл от пользователя
    :param session: AsyncSession: Создайте подключение к базе данных
    """
    if in_file.filename:
        format_file = in_file.filename.split('.')[-1]
        try:
            assert(format_file == 'wav')
        except:
            raise HTTPException(status_code=400, detail={
                'status': 'error',
                'filename': None,
                'result': f'Файл формата {format_file} не подерживается. Загрузите аудио файл формата .wav.'
            })
    time_now = datetime.utcnow()
    time_now_strftime = time_now.strftime('%d_%m_%Y__%H_%M_%S')
    new_file_name = f'{time_now_strftime}_upload_{in_file.filename}'
    out_file_path = f'wav/{new_file_name}'
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content :=  await in_file.read(1024):
            await out_file.write(content)
    f = sf.SoundFile(out_file_path)
    result_all = {'data': 'Загружается'}
    new_audio_file = AudioFileCreate(name=new_file_name, 
                                     duration=f'{f.frames/f.samplerate}', 
                                     time=time_now, 
                                     device=device_type, 
                                     result=result_all) 

    stmt = insert(audiofile).values(**new_audio_file.dict())
    await session.execute(stmt)
    await session.commit()
    # recognition_audio_files.delay(out_file_path=new_file_name)
    return {'status': 'success', 'filename': new_file_name, 'result': result_all}

@router.get('/resultfile')
async def get_result_recognition(filename: str, session: AsyncSession = Depends(get_async_session)):
    """
    Функция get_result_recognition возвращает результат распознавания для данного аудиофайла.
        Функция принимает имя файла аудио и возвращает результат распознавания в виде объекта JSON.
    
    :param filename: str: Укажите имя файла, который будет удален
    :param session: AsyncSession: Передать сеанс функции
    :return: объект json, содержащий результат распознавания
    """
    query = select(audiofile.c.result).where(audiofile.c.name == filename)
    result = await session.execute(query)
    a = [r._mapping for r in result][0]
    return {'result': a['result']}

@router.get('/download')
def get_audio_file(filename: str):
    """
    Функция get_audio_file возвращает объект ответа File, содержащий аудиофайл.
        Функция принимает имя файла в качестве аргумента и возвращает соответствующий аудиофайл.
    
    :param filename: str: Укажите имя файла, который будет воспроизводиться
    :return: Объект fileresponse
    """
    return FileResponse(f'wav/{filename}')

