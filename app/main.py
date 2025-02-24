import os

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request
from pathlib import Path

from app import crud
from .database import engine, Base, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
static_dir = os.path.join(BASE_DIR.parent, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@app.post("/items/")
def create_new_item(name: str,
                    description: str = None,
                    db: Session = Depends(get_db)):
    return crud.create_item(db, name, description)


@app.get("/test_db/")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Попробуем выполнить простой запрос для проверки соединения
        db.execute("SELECT 1")
        return {"status": "Database connection is working!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}
