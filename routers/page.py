from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="./templates")


@router.get("/")
def index(request: Request):
    name = "xiran"
    return templates.TemplateResponse("index.html", locals())
