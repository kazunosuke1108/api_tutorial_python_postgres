# schemas.py
# FastAPI の入出力で使う型。リクエスト用（Create/Update）とレスポンス用（Read）を分けるのが定石。
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


# sex は DB の CHECK 制約と合わせて Literal で表現
SexLiteral = Literal["male", "female", "other", "unknown"]


# -------- Patients --------
class PatientBase(BaseModel):
    name: str = Field(..., max_length=50)
    age: int = Field(..., ge=0)  # chk_patients_age_nonneg と整合
    sex: SexLiteral


class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    # 部分更新用（必要に応じて）
    name: Optional[str] = Field(None, max_length=50)
    age: Optional[int] = Field(None, ge=0)
    sex: Optional[SexLiteral] = None


class PatientRead(BaseModel):
    # DBから返すときの形（idやタイムスタンプを含む）
    model_config = ConfigDict(from_attributes=True)  # ORM モード（v2系）
    id: int
    name: str
    age: int
    sex: SexLiteral
    created_at: datetime
    updated_at: datetime


# -------- Vital Logs --------
class VitalLogBase(BaseModel):
    body_temperature: Optional[Decimal] = Field(
        None, ge=30.0, le=45.0
    )  # chk_temp_range と整合
    description: Optional[str] = Field(None, max_length=200)
    measured_at: Optional[datetime] = None  # 未指定ならサーバ側/DB側で now()


class VitalLogCreate(VitalLogBase):
    patient_id: int  # 紐付け必須


class VitalLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    patient_id: int
    body_temperature: Optional[Decimal]
    description: Optional[str]
    created_at: datetime
    measured_at: datetime
