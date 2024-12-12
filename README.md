# fastapi-chatbot-api

## How to run
```bash
pip install -r requirements.txt
uvicorn uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Deployed Railway: https://web-production-65db.up.railway.app/docs

## How to test
```bash
pytest tests/
```

## How to migration
```bash
alembic init alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```