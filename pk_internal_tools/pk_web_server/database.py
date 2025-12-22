from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import logging
import traceback
from pathlib import Path

# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# Initialize logging
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

# 데이터베이스 파일 경로 정의
DATABASE_FILE = Path(__file__).parent.parent.parent.parent / ".pk_system" / "pk_databases" / "pk_web_server.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# 데이터베이스 디렉토리 생성 확인
DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
logger.info(f"Database will be stored at: {DATABASE_FILE}")

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 선언적 베이스 생성
Base = declarative_base()

class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Memo(id={self.id}, title='{self.title[:20]}...')>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

# 데이터베이스 테이블 생성
def create_db_and_tables():
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
        traceback.print_exc()

# 의존성 주입을 위한 DB 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_db_and_tables()
    logger.info("Database setup complete.")
