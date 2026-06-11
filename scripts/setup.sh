#!/bin/bash

set -e

echo "🚀 Setting up SentinelMind AI Platform"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

command -v python3 >/dev/null 2>&1 || { echo -e "${RED}Python 3 is required but not installed.${NC}" >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo -e "${RED}Node.js is required but not installed.${NC}" >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo -e "${RED}Docker is required but not installed.${NC}" >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo -e "${RED}Docker Compose is required but not installed.${NC}" >&2; exit 1; }

echo -e "${GREEN}✓ Prerequisites satisfied${NC}"

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
cd backend
pip install --upgrade pip
pip install -r requirements/base.txt
pip install -r requirements/ml.txt
cd ..

# Install frontend dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
cd frontend
npm install
cd ..

# Create .env files
echo -e "${YELLOW}Creating environment files...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.local.example frontend/.env.local
    echo -e "${GREEN}✓ Created frontend .env.local file${NC}"
fi

# Generate secure keys
echo -e "${YELLOW}Generating secure keys...${NC}"
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

sed -i "s/your-super-secret-key-change-this/$SECRET_KEY/g" .env
sed -i "s/your-jwt-secret-key/$JWT_SECRET/g" .env

echo -e "${GREEN}✓ Generated secure keys${NC}"

# Download spaCy model
echo -e "${YELLOW}Downloading spaCy model...${NC}"
python -m spacy download en_core_web_sm

# Setup database
echo -e "${YELLOW}Setting up database...${NC}"
docker-compose up -d postgres redis
sleep 10

cd backend
alembic upgrade head
cd ..

echo -e "${GREEN}✓ Database setup complete${NC}"

# Train models (optional)
read -p "Do you want to train ML models? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Training ML models...${NC}"
    cd backend
    python training/train_sentiment.py --epochs 5 --batch_size 16
    python training/train_emotion.py --epochs 5 --batch_size 16
    cd ..
fi

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Update the .env file with your configuration"
echo "2. Run 'docker-compose up -d' to start all services"
echo "3. Access the application at http://localhost:3000"
echo "4. API documentation available at http://localhost:8000/api/docs"