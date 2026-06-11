-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types
CREATE TYPE user_role AS ENUM ('user', 'premium', 'admin', 'super_admin');
CREATE TYPE analysis_type AS ENUM ('sentiment', 'emotion', 'toxicity', 'comprehensive');

-- Create indexes for performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_analyses_user_id_created_at ON analyses(user_id, created_at);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_analyses_sentiment_label ON analyses(sentiment_label);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_username ON users(username);

-- Create function for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();