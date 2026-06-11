FROM postgres:15-alpine

# Install additional extensions
RUN apk add --no-cache postgresql-contrib

# Copy custom initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/

# Set custom configuration
RUN echo "shared_buffers = 256MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "effective_cache_size = 768MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "maintenance_work_mem = 64MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "work_mem = 4MB" >> /usr/local/share/postgresql/postgresql.conf.sample

EXPOSE 5432

CMD ["postgres"]