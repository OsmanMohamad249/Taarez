#!/bin/bash
# Taarez Infrastructure Setup Script
# This script sets up the development environment for Taarez

set -e

echo "=============================================="
echo "Taarez Infrastructure Setup"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi
print_success "Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
print_success "Docker Compose is installed"

echo ""
echo "Setting up environment files..."
echo ""

# Setup root .env file
if [ ! -f .env ]; then
    print_info "Creating root .env file..."
    cp .env.example .env
    
    # Generate a strong secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    
    # Update the secret key in .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    fi
    
    print_success "Root .env file created with generated SECRET_KEY"
else
    print_warning "Root .env file already exists, skipping..."
fi

# Setup backend .env file
if [ ! -f backend/.env ]; then
    print_info "Creating backend .env file..."
    cp backend/.env.example backend/.env
    
    # Generate a strong secret key for backend
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -base64 32)
    
    # Update the secret key in backend/.env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" backend/.env
    else
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" backend/.env
    fi
    
    print_success "Backend .env file created with generated SECRET_KEY"
else
    print_warning "Backend .env file already exists, skipping..."
fi

# Setup admin-portal .env file
if [ ! -f admin-portal/.env ]; then
    print_info "Creating admin-portal .env file..."
    cp admin-portal/.env.example admin-portal/.env
    print_success "Admin-portal .env file created"
else
    print_warning "Admin-portal .env file already exists, skipping..."
fi

echo ""
echo "Validating backend environment..."
echo ""

# Validate backend environment
cd backend
if python3 validate_env.py; then
    print_success "Backend environment validation passed"
else
    print_error "Backend environment validation failed"
    print_info "Please check backend/.env and update the values"
    exit 1
fi
cd ..

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Start the infrastructure: docker compose up -d"
echo "2. Check logs: docker compose logs -f"
echo "3. Access backend API: http://localhost:8000/docs"
echo "4. Access admin portal: Install dependencies first with 'cd admin-portal && npm install', then run 'npm run dev'"
echo ""
echo "For more information, see README.md"
