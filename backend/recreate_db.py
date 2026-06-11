import asyncio
from app.core.database import engine, Base
from app.models.user import User
from app.models.analysis import Analysis
from app.models.feedback import Feedback
from app.models.api_key import APIKey
from app.models.audit_log import AuditLog
from app.models.model_metadata import ModelMetadata

async def recreate_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables recreated successfully!")

if __name__ == "__main__":
    asyncio.run(recreate_db())