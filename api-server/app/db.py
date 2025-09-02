# app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# docker-compose の environment で渡した DATABASE_URL を使う
# 例: postgresql+psycopg2://appuser:apppass@postgres:5432/appdb
DATABASE_URL = os.getenv("DATABASE_URL")

# エンジン作成
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 死んだ接続を自動検知
)

# セッションファクトリ
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 依存性注入用のヘルパ（FastAPIで使う）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
