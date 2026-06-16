from typing import List, Optional
from fastapi import Request, HTTPException, Depends
from core.logging import logger
from models.user import User, UserRole
from api.deps import get_current_user

def log_unauthorized_access(request: Request, user_id: Optional[str], role: Optional[str]):
    log_data = {
        "event": "unauthorized_access",
        "user_id": user_id,
        "role": role,
        "requested_resource": request.url.path,
        "requested_action": request.method,
        "result": "DENIED"
    }
    logger.warning("Unauthorized access attempt", extra=log_data)

class RequireRoles:
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles
        
    async def __call__(self, request: Request, current_user: User = Depends(get_current_user)):
        with open("rbac_debug.txt", "a") as f:
            f.write(f"current_user.role={repr(current_user.role)}, allowed={[repr(r) for r in self.allowed_roles]}\n")
        if current_user.role not in self.allowed_roles:
            log_unauthorized_access(
                request=request, 
                user_id=str(current_user.id) if current_user else None, 
                role=current_user.role if current_user else None
            )
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user

async def enforce_deny_by_default(request: Request):
    route = request.scope.get("route")
    if not route:
        return
        
    public_paths = [
        "/api/v1/health",
        "/api/v1/auth/login"
    ]
    
    # Allow docs, openapi, and whitelisted API paths
    if request.url.path in public_paths or not request.url.path.startswith("/api/"):
        return
        
    has_rbac = False
    
    # Check dependencies at the route level
    if hasattr(route, "dependencies"):
        for dep in route.dependencies:
            if hasattr(dep.dependency, "__class__") and dep.dependency.__class__.__name__ == "RequireRoles":
                has_rbac = True
                break
                
    # Check dependencies in function parameters
    if not has_rbac and hasattr(route, "dependant") and hasattr(route.dependant, "dependencies"):
        for dep in route.dependant.dependencies:
            if hasattr(dep.call, "__class__") and dep.call.__class__.__name__ == "RequireRoles":
                has_rbac = True
                break
                
    if not has_rbac:
        log_unauthorized_access(request, user_id="system", role="unprotected_route")
        raise HTTPException(status_code=403, detail="Access denied by default. Route is unprotected.")
