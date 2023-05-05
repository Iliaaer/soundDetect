from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.audiofiles.router import get_all_name_audio_file, post_audio_file

router = APIRouter(
    prefix='',
    tags=['Pages']
)

templates = Jinja2Templates(directory='src/templates')

@router.post('/uploadfiles/{device_type}')
def post_upload_file(request: Request, file=Depends(post_audio_file)):
    """
    Функция post_upload_file используется для загрузки файла на сервер.
        Функция принимает объект запроса и аудиофайл, который затем сохраняется на сервере.
        Функция возвращает ответ перенаправления, который отправляет пользователя обратно в /allaudio/local.
    
    :param request: Запрос: Получение объекта запроса
    :param file: Получить файл из запроса
    :return: Перенаправление ответа на локальный маршрут /allaudio/
    """
    return RedirectResponse('/allaudio/local', status_code=302)

# @router.get('/base')
# def get_base_page(request: Request):
#     return templates.TemplateResponse('base.html', {'request': request})

@router.get('/')
def get_home(request: Request):
    """
    Функция get_home - это функция просмотра, которая возвращает домашнюю страницу веб-сайта.
        Он принимает объект запроса и возвращает HTML-ответ с шаблоном домашней страницы.
    
    :param request: Запрос: Передать объект запроса шаблону
    :return: Объект ответа шаблона
    """
    return templates.TemplateResponse('home.html', {'request': request})

@router.get('/allaudio/{device_type}')
def get_all_audio(request: Request, allnames: dict=Depends(get_all_name_audio_file)):
    """
    Функция get_all_audio возвращает список всех аудиофайлов в базе данных.
        
    :param request: Запрос: Получение объекта запроса
    :param allnames: dict: Передать словарь всех имен и аудиофайлов в шаблон
    :return: Объект templateresponse
    """
    return templates.TemplateResponse('allaudio.html', {'request': request, 'allnames': allnames['result']})
