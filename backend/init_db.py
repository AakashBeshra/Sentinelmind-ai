import asyncio
from app.core.database import engine, Base
from app.models.user import User
from app.models.analysis import Analysis
from app.models.feedback import Feedback
from app.models.api_key import APIKey
from app.models.audit_log import AuditLog
from app.models.model_metadata import ModelMetadata
async def init_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	print('Database tables created succesfully!')
if __name__ == "__main__":
	asyncio.run(init_db())