from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Указание пути к папке с шаблонами
templates = Jinja2Templates(directory="templates")

# Подключаем папку static для обслуживания статических файлов (например, favicon.ico)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Рендерим шаблон index.html
    return templates.TemplateResponse("index.html", {"request": request})
