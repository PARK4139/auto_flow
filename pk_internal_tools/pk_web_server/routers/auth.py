from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import logging
import traceback

from jose import JWTError, jwt
from passlib.context import CryptContext

# Lazy import for ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized

# Initialize logging for the router
ensure_pk_system_log_initialized(__file__)
logger = logging.getLogger(__name__)

router = APIRouter()

# --- 설정 ---
# 설정 값은 외부에서 주입받도록 변경 (순환 임포트 방지)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# tokenUrl은 main.py에서 설정될 것이므로, 여기서는 임시로 "/auth/token"으로 유지
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") 

# --- Pydantic 모델 ---
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
    hashed_password: str # 실제 DB에서는 해시된 비밀번호만 저장

class UserInDB(User):
    pass # 추가 정보 필요시 확장

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# --- 임시 사용자 저장소 (실제 DB로 대체 예정) ---
_users_db = {} # username: UserInDB

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# SECRET_KEY와 ALGORITHM을 인자로 받도록 수정
def create_access_token(data: dict, secret_key: str, algorithm: str, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # ACCESS_TOKEN_EXPIRE_MINUTES를 외부에서 주입받도록 변경
        # 여기서는 임시 기본값 사용 (main.py에서 주입)
        expire = datetime.utcnow() + timedelta(minutes=30) # pk_option: Replace with injected value
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# authenticate_user 함수는 변경 없음 (SECRET_KEY, ALGORITHM 사용 안함)
async def authenticate_user(username: str, password: str):
    user = _users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# SECRET_KEY와 ALGORITHM을 인자로 받도록 수정
async def get_current_user(token: str = Depends(oauth2_scheme), secret_key: str = Depends(lambda: router.secret_key), algorithm: str = Depends(lambda: router.algorithm)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = _users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# get_current_active_user 함수는 변경 없음 (SECRET_KEY, ALGORITHM 사용 안함)
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# --- 엔드포인트 ---
@router.post("/register", response_model=User, summary="사용자 등록 (회원가입)", tags=["Auth"])
async def register_user(user_create: UserCreate):
    """
    새로운 사용자를 등록합니다.
    - **username**: 사용자 이름 (필수)
    - **password**: 비밀번호 (필수)
    - **email**: 이메일 (선택)
    - **full_name**: 전체 이름 (선택)
    """
    if _users_db.get(user_create.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = get_password_hash(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_password
    )
    _users_db[new_user.username] = new_user
    logger.info(f"새 사용자 등록: {new_user.username}")
    return new_user

@router.post("/token", response_model=Token, summary="JWT 액세스 토큰 발급", tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), secret_key: str = Depends(lambda: router.secret_key), algorithm: str = Depends(lambda: router.algorithm), access_token_expire_minutes: int = Depends(lambda: router.access_token_expire_minutes)):
    """
    사용자 이름과 비밀번호로 로그인하여 JWT 액세스 토큰을 발급받습니다.
    - **username**: 사용자 이름
    - **password**: 비밀번호
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, secret_key=secret_key, algorithm=algorithm, expires_delta=access_token_expires
    )
    logger.info(f"사용자 {user.username} 로그인 성공, 토큰 발급.")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User, summary="현재 로그인 사용자 정보 조회", tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    현재 로그인한 사용자 정보를 조회합니다. (JWT 토큰 필요)
    """
    logger.info(f"사용자 {current_user.username} 정보 조회 요청.")
    return current_user