#!/bin/bash

set -e

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "Starting backup at $TIMESTAMP"

# Backup PostgreSQL
echo "Backing up database..."
docker exec sentinelmind-postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > $BACKUP_DIR/db_$TIMESTAMP.sql.gz

# Backup Redis
echo "Backing up Redis..."
docker exec sentinelmind-redis redis-cli --rdb /data/dump.rdb
docker cp sentinelmind-redis:/data/dump.rdb $BACKUP_DIR/redis_$TIMESTAMP.rdb

# Backup models
echo "Backing up ML models..."
tar -czf $BACKUP_DIR/models_$TIMESTAMP.tar.gz models/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup complete!"