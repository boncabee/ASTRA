from fastapi import APIRouter, Depends
from core.rbac import RequireRoles
from models.user import UserRole

router = APIRouter(
    dependencies=[Depends(RequireRoles([UserRole.ADMINISTRATOR, UserRole.SECURITY_ENGINEER]))]
)

@router.get("/ping")
async def security_ping():
    return {"message": "pong", "role": "security"}
