#!/bin/bash

set -e

echo "Initializing database..."

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing migrations"

# Run Alembic migrations
cd backend
alembic upgrade head

# Seed initial data
python -c "
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
if not db.query(User).filter(User.email == 'admin@sentinelmind.ai').first():
    admin = User(
        email='admin@sentinelmind.ai',
        username='admin',
        full_name='Admin User',
        hashed_password=get_password_hash('Admin123!'),
        role='super_admin',
        is_active=True,
        is_verified=True
    )
    db.add(admin)
    db.commit()
    print('Admin user created')
db.close()
"

echo "Database initialization complete!"