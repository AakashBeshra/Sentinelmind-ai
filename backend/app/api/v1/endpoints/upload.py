from fastapi import APIRouter, Depends, UploadFile, File
from app.api.deps import get_current_active_user
from app.models.user import User
router = APIRouter()
@router.post("/file")
async def upload_file(
    file: UploadFile= File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a file for analysis"""
    return {"filename": file.filename, "message": "File uploaded"}