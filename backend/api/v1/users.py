import uuid
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_db
from core.rbac import RequireRoles
from core.security import get_password_hash
from models.user import User, UserRole
from schemas.user import (
    UserCreate, UserUpdate, UserStatusUpdate, UserRoleUpdate, 
    UserResponseWrapper, UserListWrapper
)
from api.deps import get_current_user

router = APIRouter()

def error_response(msg: str, code: int):
    return JSONResponse(status_code=code, content={"error": msg, "code": code})

# Roles configured from architectural matrix
read_roles = [UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER, UserRole.INCIDENT_RESPONDER, UserRole.SOC_ANALYST]
write_roles = [UserRole.ADMINISTRATOR]

@router.get("", response_model=UserListWrapper, dependencies=[Depends(RequireRoles(read_roles))])
async def list_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"data": users}

@router.get("/{user_id}", response_model=UserResponseWrapper, dependencies=[Depends(RequireRoles(read_roles))])
async def get_user(user_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await db.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
    return {"data": user}

@router.post("", response_model=UserResponseWrapper, dependencies=[Depends(RequireRoles(write_roles))])
async def create_user(
    user_in: UserCreate, 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    stmt = select(User).where((User.username == user_in.username) | (User.email == user_in.email))
    result = await db.execute(stmt)
    if result.scalars().first():
        return error_response("Username or email already exists", 400)
        
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active,
        created_by=str(current_user.id),
        updated_by=str(current_user.id)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"data": db_user}

@router.put("/{user_id}", response_model=UserResponseWrapper, dependencies=[Depends(RequireRoles(write_roles))])
async def update_user(
    user_id: uuid.UUID,
    user_in: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    user = await db.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
        
    if user_in.username and user_in.username != user.username:
        stmt = select(User).where(User.username == user_in.username)
        res = await db.execute(stmt)
        if res.scalars().first():
            return error_response("Username already exists", 400)
        user.username = user_in.username
        
    if user_in.email and user_in.email != user.email:
        stmt = select(User).where(User.email == user_in.email)
        res = await db.execute(stmt)
        if res.scalars().first():
            return error_response("Email already exists", 400)
        user.email = user_in.email

    user.updated_by = str(current_user.id)
    await db.commit()
    await db.refresh(user)
    return {"data": user}

@router.patch("/{user_id}/status", response_model=UserResponseWrapper, dependencies=[Depends(RequireRoles(write_roles))])
async def update_status(
    user_id: uuid.UUID,
    status_in: UserStatusUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    user = await db.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
        
    user.is_active = status_in.is_active
    user.updated_by = str(current_user.id)
    await db.commit()
    await db.refresh(user)
    return {"data": user}

@router.patch("/{user_id}/role", response_model=UserResponseWrapper, dependencies=[Depends(RequireRoles(write_roles))])
async def update_role(
    user_id: uuid.UUID,
    role_in: UserRoleUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    user = await db.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
        
    user.role = role_in.role
    user.updated_by = str(current_user.id)
    await db.commit()
    await db.refresh(user)
    return {"data": user}
