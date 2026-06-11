import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from datetime import datetime
import bcrypt

DATABASE_URL = "sqlite+aiosqlite:///./sentinelmind.db"

async def create_user():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Hash the password
    password = "Test123!"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    async with engine.begin() as conn:
        # Check if user exists
        result = await conn.execute(text("SELECT id FROM users WHERE email = 'test@example.com'"))
        existing = result.fetchone()
        
        if existing:
            print("User already exists!")
            return
        
        # Insert user
        await conn.execute(text("""
            INSERT INTO users (email, username, full_name, hashed_password, is_active, is_verified, created_at, updated_at)
            VALUES (:email, :username, :full_name, :password, 1, 1, :now, :now)
        """), {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": hashed,
            "now": datetime.now()
        })
        
        print("✓ User created successfully!")
        print("Email: test@example.com")
        print("Password: Test123!")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_user())
