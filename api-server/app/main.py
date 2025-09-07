# app/main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field, ConfigDict, conint, constr
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

from .db import get_db
from .model import Patient, VitalLog
from .schemas import PatientCreate, PatientRead, PatientUpdate

app = FastAPI(title="Calc Engine API")

# CRUD
## Create: 患者登録
@app.post("/add-patient",response_model=PatientCreate)
def add_patient(patient: PatientCreate, db: Session=Depends(get_db)):
    db.execute(
        text("INSERT INTO patients (name, age, sex) VALUES (:name, :age, :sex)"),
        {"name": patient.name, "age": patient.age, "sex": patient.sex}
    )
    db.commit()
    return patient

## Read: 患者一覧取得
@app.get("/get-patients", response_model=list[PatientRead])
def get_patients(db: Session=Depends(get_db)):
    rows = db.execute(
        text("SELECT * FROM patients")
    ).mappings().all()
    return [PatientRead(**r) for r in rows]

## Read (登録日期間指定): 患者一覧取得
@app.get("/get-patients-by-date", response_model=list[PatientRead])
def get_patients_by_date(start_date: str, end_date: str, db: Session=Depends(get_db)):
    # ISO 8601 形式の文字列 ("2025-09-01T00:00:00") を datetime に変換
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)
    rows = db.execute(
        text("SELECT * FROM patients WHERE created_at BETWEEN :start_date AND :end_date"),
        {"start_date": start_dt, "end_date": end_dt}
    ).mappings().all()
    return [PatientRead(**r) for r in rows]

## Update: 患者情報更新
@app.put("/update-patient/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: int, patient: PatientUpdate, db: Session=Depends(get_db)):
    db.execute(
        text("UPDATE patients SET name = :name, age = :age, sex = :sex WHERE id = :id"),
        {"name": patient.name, "age": patient.age, "sex": patient.sex, "id": patient_id}
    )
    db.commit()
    return db.execute(
        text("SELECT * FROM patients WHERE id = :id"),
        {"id": patient_id}
    ).mappings().one()

## Delete: 患者削除
@app.delete("/delete-patient/{patient_id}")
def delete_patient(patient_id: int, db: Session=Depends(get_db)):
    db.execute(
        text("DELETE FROM patients WHERE id = :id"),
        {"id": patient_id}
    )
    db.commit()
    return {"message": "patient deleted"}

# class Person(BaseModel):
#     name: constr(min_length=1) = Field(..., description="名前")
#     age: conint(ge=0, le=150) = Field(..., description="年齢(0-150)")
#     # Swagger の Example を表示
#     model_config = ConfigDict(json_schema_extra={
#         "example": {"name": "Alice", "age": 25}
#     })

# @app.get("/healthz")
# def healthz():
#     return {"status": "ok"}

# @app.get("/tasks")
# def list_tasks(db: Session = Depends(get_db)):
#     """
#     tasks テーブルを取得して返す最小API。
#     SQLAlchemy Coreの text() を使ってシンプルに取得。
#     """
#     rows = db.execute(
#         text("SELECT id, name, age FROM users ORDER BY id DESC")
#     ).mappings().all()  # .mappings() で dict 風アクセス
#     # list[dict] にして返す
#     return [dict(r) for r in rows]

# @app.post("/add_people", tags=["users"], summary="ユーザーを追加")
# def add_people(person: Person, db: Session = Depends(get_db)):
#     db.execute(
#         text("INSERT INTO users (name, age) VALUES (:name, :age)"),
#         {"name": person.name, "age": person.age}
#     )
#     db.commit()
#     return {"message": "person added", "person": person.model_dump()}
