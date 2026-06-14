from fastapi import APIRouter, Depends
from core.rbac import RequireRoles
from models.user import UserRole

router = APIRouter(
    dependencies=[Depends(RequireRoles([UserRole.ADMINISTRATOR, UserRole.INCIDENT_RESPONDER]))]
)

@router.get("/ping")
async def responders_ping():
    return {"message": "pong", "role": "responders"}
