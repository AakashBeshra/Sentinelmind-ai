from fastapi import APIRouter, Depends
from app.api.deps import get_current_active_user
from app.models.user import User
router = APIRouter()
@router.post("/extract")
async def extract_text(
    current_user: User = Depends(get_current_active_user)
):
    """Extract text from image"""
    return {"message": "OCR extraction endpoint"}