python -m venv venv

venv\Scripts\activate

pip freeze > requirements.txt

pip install -r requirements.txt

cd E:\Need_Programs\PycharmProjects\nomad-fastapi
uvicorn app.main:app --reload
