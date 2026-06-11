import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "sqlite+aiosqlite:///./sentinelmind.db"

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # Create users table directly
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(255) NOT NULL UNIQUE,
                username VARCHAR(50) NOT NULL UNIQUE,
                full_name VARCHAR(100),
                hashed_password VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                is_verified BOOLEAN DEFAULT 0,
                role VARCHAR(20) DEFAULT 'user',
                avatar_url VARCHAR(500),
                api_calls_limit INTEGER DEFAULT 1000,
                api_calls_used INTEGER DEFAULT 0,
                premium_until DATETIME,
                total_analyses INTEGER DEFAULT 0,
                last_active DATETIME,
                last_password_change DATETIME,
                failed_login_attempts INTEGER DEFAULT 0,
                locked_until DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create analyses table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                original_text TEXT NOT NULL,
                cleaned_text TEXT,
                language VARCHAR(10),
                analysis_type VARCHAR(20),
                sentiment_label VARCHAR(20),
                sentiment_confidence FLOAT,
                sentiment_scores JSON,
                emotions JSON,
                dominant_emotion VARCHAR(20),
                emotion_confidence FLOAT,
                toxicity_score FLOAT,
                is_toxic BOOLEAN DEFAULT 0,
                entities JSON,
                processing_time_ms FLOAT,
                model_version VARCHAR(50),
                batch_id VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """))
        
        print("✓ Database tables created successfully!")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())