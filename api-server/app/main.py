# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from .db import get_db

app = FastAPI(title="Calc Engine API")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    """
    tasks テーブルを取得して返す最小API。
    SQLAlchemy Coreの text() を使ってシンプルに取得。
    """
    rows = db.execute(
        text("SELECT id, name, age FROM users ORDER BY id DESC")
    ).mappings().all()  # .mappings() で dict 風アクセス
    # list[dict] にして返す
    return [dict(r) for r in rows]
