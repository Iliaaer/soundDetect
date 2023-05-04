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
    return RedirectResponse('/allaudio/local', status_code=302)

@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})

@router.get('/')
def get_home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@router.get('/allaudio/{device_type}')
def get_all_audio(request: Request, allnames: dict=Depends(get_all_name_audio_file)):
    return templates.TemplateResponse('allaudio.html', {'request': request, 'allnames': allnames['result']})
