from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import traceback
from datetime import datetime
from sqlalchemy.orm import Session # Session 임포트

# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# pk_web_server.database에서 get_db와 Memo ORM 모델 임포트
from ..database import get_db, Memo as ORMMemo

# Initialize logging for the router
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Memo 모델 정의 (ORM 모델과 호환되도록 from_attributes = True 추가)
class Memo(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Pydantic v2
        # from_orm = True # Pydantic v1 (이전 버전 호환성)

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# 인메모리 데이터베이스 관련 코드 제거
# _in_memory_memos_db = {}
# _next_memo_id = 1

from sqlalchemy.orm import Session # 추가
from sqlalchemy import desc # 추가

class MemoRepository:
    """
    메모 데이터베이스 접근 계층 (Repository / DAO)
    SQLAlchemy를 통해 실제 데이터베이스 로직이 구현됩니다.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ORMMemo]:
        logger.debug("Repository: 모든 메모 조회")
        return self.db.query(ORMMemo).order_by(desc(ORMMemo.created_at)).all()

    def get_by_id(self, memo_id: int) -> Optional[ORMMemo]:
        logger.debug(f"Repository: ID {memo_id} 메모 조회")
        return self.db.query(ORMMemo).filter(ORMMemo.id == memo_id).first()

    def create(self, memo_create: MemoCreate) -> ORMMemo:
        logger.debug(f"Repository: 새 메모 생성 (제목: {memo_create.title})")
        db_memo = ORMMemo(
            title=memo_create.title,
            content=memo_create.content,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.add(db_memo)
        self.db.commit()
        self.db.refresh(db_memo)
        return db_memo

    def update(self, memo_id: int, memo_update: MemoUpdate) -> Optional[ORMMemo]:
        logger.debug(f"Repository: ID {memo_id} 메모 업데이트")
        db_memo = self.db.query(ORMMemo).filter(ORMMemo.id == memo_id).first()
        if db_memo:
            update_data = memo_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_memo, key, value)
            db_memo.updated_at = datetime.now()
            self.db.commit()
            self.db.refresh(db_memo)
            return db_memo
        return None

    def delete(self, memo_id: int) -> bool:
        logger.debug(f"Repository: ID {memo_id} 메모 삭제")
        db_memo = self.db.query(ORMMemo).filter(ORMMemo.id == memo_id).first()
        if db_memo:
            self.db.delete(db_memo)
            self.db.commit()
            return True
        return False


class MemoService:
    """
    메모 관련 비즈니스 로직 계층 (Service / UseCase)
    """
    def __init__(self, db: Session = Depends(get_db)): # DB 세션 주입
        self.repository = MemoRepository(db) # DB 세션으로 Repository 초기화

    def get_all_memos(self) -> List[Memo]:
        logger.debug("Service: 모든 메모 조회")
        orm_memos = self.repository.get_all()
        return [Memo.model_validate(memo) for memo in orm_memos] # Pydantic 모델로 변환

    def get_memo_by_id(self, memo_id: int) -> Optional[Memo]:
        logger.debug(f"Service: ID {memo_id} 메모 조회")
        orm_memo = self.repository.get_by_id(memo_id)
        return Memo.model_validate(orm_memo) if orm_memo else None # Pydantic 모델로 변환

    def create_new_memo(self, memo_create: MemoCreate) -> Memo:
        logger.debug(f"Service: 새 메모 생성 (제목: {memo_create.title})")
        orm_memo = self.repository.create(memo_create)
        return Memo.model_validate(orm_memo) # Pydantic 모델로 변환

    def update_memo_data(self, memo_id: int, memo_update: MemoUpdate) -> Optional[Memo]:
        logger.debug(f"Service: ID {memo_id} 메모 업데이트")
        orm_memo = self.repository.update(memo_id, memo_update)
        return Memo.model_validate(orm_memo) if orm_memo else None # Pydantic 모델로 변환

    def delete_memo_data(self, memo_id: int) -> bool:
        logger.debug(f"Service: ID {memo_id} 메모 삭제")
        return self.repository.delete(memo_id)

@router.get("/memos", response_model=List[Memo], summary="모든 메모 조회", tags=["Memos"])
async def get_all_memos(memo_service: MemoService = Depends()):
    """
    저장된 모든 메모를 조회합니다.
    """
    logger.info("Router: 모든 메모 조회 요청이 들어왔습니다.")
    return memo_service.get_all_memos() # 이미 MemoService에서 Pydantic 모델로 변환되어 반환

@router.get("/memos/{memo_id}", response_model=Memo, summary="특정 메모 조회", tags=["Memos"])
async def get_memo(memo_id: int, memo_service: MemoService = Depends()):
    """
    특정 ID를 가진 메모를 조회합니다.
    - **memo_id**: 조회할 메모의 ID
    """
    logger.info(f"Router: {memo_id} ID를 가진 메모 조회 요청이 들어왔습니다.")
    memo = memo_service.get_memo_by_id(memo_id)
    if memo:
        return memo
    logger.warning(f"Router: 메모 ID {memo_id}를 찾을 수 없습니다.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")

@router.post("/memos", response_model=Memo, status_code=status.HTTP_201_CREATED, summary="새 메모 생성", tags=["Memos"])
async def create_memo(memo_create: MemoCreate, memo_service: MemoService = Depends()):
    """
    새로운 메모를 생성합니다.
    - **title**: 메모의 제목
    - **content**: 메모의 내용
    """
    logger.info(f"Router: 새 메모 생성 요청 받음 (제목: {memo_create.title})")
    new_memo = memo_service.create_new_memo(memo_create)
    logger.info(f"Router: 새 메모 생성 완료: ID {new_memo.id}")
    return new_memo


@router.put("/memos/{memo_id}", response_model=Memo, summary="메모 업데이트", tags=["Memos"])
async def update_memo(memo_id: int, memo_update: MemoUpdate, memo_service: MemoService = Depends()):
    """
    특정 ID를 가진 메모를 업데이트합니다.
    - **memo_id**: 업데이트할 메모의 ID
    - **memo_update**: 업데이트할 내용 (제목, 내용 중 하나 이상)
    """
    logger.info(f"Router: ID {memo_id} 메모 업데이트 요청 받음.")
    updated_memo = memo_service.update_memo_data(memo_id, memo_update)
    if updated_memo:
        logger.info(f"Router: ID {memo_id} 메모 업데이트 성공.")
        return updated_memo
    logger.warning(f"Router: 메모 ID {memo_id}를 찾을 수 없어 업데이트 실패.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")


@router.delete("/memos/{memo_id}", status_code=status.HTTP_204_NO_CONTENT, summary="메모 삭제", tags=["Memos"])
async def delete_memo(memo_id: int, memo_service: MemoService = Depends()):
    """
    특정 ID를 가진 메모를 삭제합니다.
    - **memo_id**: 삭제할 메모의 ID
    """
    logger.info(f"Router: ID {memo_id} 메모 삭제 요청 받음.")
    success = memo_service.delete_memo_data(memo_id)
    if success:
        logger.info(f"Router: ID {memo_id} 메모 삭제 성공.")
        return # 204 No Content
    logger.warning(f"Router: 메모 ID {memo_id}를 찾을 수 없어 삭제 실패.")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memo not found")