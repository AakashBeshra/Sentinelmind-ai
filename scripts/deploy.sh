#!/bin/bash

set -e

echo "🚀 Deploying SentinelMind AI to Production"

# Load environment variables
source .env

# Pull latest images
echo "Pulling latest Docker images..."
docker-compose -f docker-compose.prod.yml pull

# Backup database
echo "Backing up database..."
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup_$(date +%Y%m%d_%H%M%S).sql

# Run migrations
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head

# Deploy services
echo "Deploying services..."
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Health check
echo "Performing health check..."
sleep 10

if curl -f http://localhost/health; then
    echo "✅ Deployment successful!"
else
    echo "❌ Health check failed. Rolling back..."
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml up -d
    exit 1
fi

# Cleanup old images
echo "Cleaning up old Docker images..."
docker system prune -f

echo "✅ Deployment complete!"