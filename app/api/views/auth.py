from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from app.api.repositories.auth import AuthRepository
from app.api.schemas.auth import UserCreate, UserResponse, Token, LoginRequest
from app.api.models.user import User
from app.core.database.config import get_general_session
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_general_session),
):
    repo = AuthRepository(session)

    if await repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    if await repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role.lower(),  # Convert to lowercase
        is_active=True,
    )
    created_user = await repo.create_user(new_user)
    return created_user


@router.post("/login", response_model=Token)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_general_session),
):
    repo = AuthRepository(session)
    user = await repo.get_by_username(data.username)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({
        "sub": str(user.id),
        "full_name": user.full_name,
        "username": user.username,
        "role": user.role.lower()  # Convert to lowercase
    })
    return Token(access_token=access_token, token_type="bearer")
