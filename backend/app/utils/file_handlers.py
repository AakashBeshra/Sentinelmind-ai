import aiofiles
import os
from pathlib import Path
from typing import BinaryIO, Optional
import hashlib

class FileHandler:
    def __init__(self, upload_dir: str = "./uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_file(self, file: BinaryIO, filename: str, subdir: str = "") -> str:
        """Save uploaded file to disk"""
        save_path = self.upload_dir / subdir
        save_path.mkdir(exist_ok=True)
        
        file_path = save_path / filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return str(file_path)
    
    async def read_file(self, file_path: str) -> str:
        """Read file content"""
        async with aiofiles.open(file_path, 'r') as f:
            return await f.read()
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from disk"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except:
            pass
        return False
    
    def get_file_hash(self, file_path: str) -> str:
        """Calculate file hash"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()