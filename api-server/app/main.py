# app/main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, ConfigDict, conint, constr
from sqlalchemy import text
from sqlalchemy.orm import Session
from .db import get_db

app = FastAPI(title="Calc Engine API")

class Person(BaseModel):
    name: constr(min_length=1) = Field(..., description="名前")
    age: conint(ge=0, le=150) = Field(..., description="年齢(0-150)")
    # Swagger の Example を表示
    model_config = ConfigDict(json_schema_extra={
        "example": {"name": "Alice", "age": 25}
    })

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

@app.post("/add_people", tags=["users"], summary="ユーザーを追加")
def add_people(person: Person, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO users (name, age) VALUES (:name, :age)"),
        {"name": person.name, "age": person.age}
    )
    db.commit()
    return {"message": "person added", "person": person.model_dump()}
