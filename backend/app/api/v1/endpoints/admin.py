from fastapi import APIRouter, Depends
from app.api.deps import get_current_admin_user
from app.models.user import User
router = APIRouter()
@router.get("/stats")
async def get_system_stats(
    admin_user: User = Depends(get_current_admin_user)
):
    """Get system statistics (admin only)"""
    return {"message": "Admin stats endpoint"}
