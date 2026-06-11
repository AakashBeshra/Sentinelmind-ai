import asyncio
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def create_user():
    async with AsyncSessionLocal() as db:
        # Check if user exists
        from sqlalchemy import select
        stmt = select(User).where(User.email == "test@example.com")
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            print("User already exists!")
            return
        
        user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password=get_password_hash("Test123!"),
            is_active=True,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        print("✓ User created successfully!")
        print("Email: test@example.com")
        print("Password: Test123!")

if __name__ == "__main__":
    asyncio.run(create_user())