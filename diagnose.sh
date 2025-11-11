#!/bin/bash
# Diagnostic script for Taarez application
# Checks all services and configurations

set -e

echo "🔍 Taarez Application Diagnostics"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Docker
echo "1. Checking Docker..."
if command -v docker &> /dev/null; then
    print_status 0 "Docker is installed"
    
    if docker ps &> /dev/null; then
        print_status 0 "Docker daemon is running"
    else
        print_status 1 "Docker daemon is not running"
    fi
else
    print_status 1 "Docker is not installed"
fi
echo ""

# Check Docker Compose
echo "2. Checking Docker Compose..."
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
    print_status 0 "Docker Compose is installed"
else
    print_status 1 "Docker Compose is not installed"
fi
echo ""

# Check if services are running
echo "3. Checking Docker services..."
if docker ps &> /dev/null; then
    BACKEND_RUNNING=$(docker ps --filter "name=backend" --format "{{.Names}}" | wc -l)
    POSTGRES_RUNNING=$(docker ps --filter "name=postgres" --format "{{.Names}}" | wc -l)
    FLUTTER_RUNNING=$(docker ps --filter "name=flutter" --format "{{.Names}}" | wc -l)
    
    print_status $((1 - BACKEND_RUNNING)) "Backend container is running"
    print_status $((1 - POSTGRES_RUNNING)) "PostgreSQL container is running"
    
    if [ $FLUTTER_RUNNING -eq 1 ]; then
        print_status 0 "Flutter container is running"
    else
        print_warning "Flutter container is not running (optional)"
    fi
else
    print_status 1 "Cannot check Docker containers"
fi
echo ""

# Check .env file
echo "4. Checking environment configuration..."
if [ -f .env ]; then
    print_status 0 ".env file exists"
    
    # Check SECRET_KEY
    if grep -q "^SECRET_KEY=" .env; then
        SECRET_KEY=$(grep "^SECRET_KEY=" .env | cut -d'=' -f2)
        if [ ${#SECRET_KEY} -ge 32 ]; then
            print_status 0 "SECRET_KEY is configured (length: ${#SECRET_KEY})"
        else
            print_status 1 "SECRET_KEY is too short (minimum 32 characters)"
        fi
    else
        print_status 1 "SECRET_KEY is not set"
    fi
    
    # Check DATABASE_URL
    if grep -q "^DATABASE_URL=" .env; then
        print_status 0 "DATABASE_URL is configured"
    else
        print_status 1 "DATABASE_URL is not set"
    fi
    
    # Check CORS_ORIGINS
    if grep -q "^CORS_ORIGINS=" .env; then
        CORS_ORIGINS=$(grep "^CORS_ORIGINS=" .env | cut -d'=' -f2)
        print_status 0 "CORS_ORIGINS is configured"
        echo "   Current: $CORS_ORIGINS"
        
        if [[ $CORS_ORIGINS == *"github.dev"* ]]; then
            print_status 0 "GitHub Codespaces URL detected in CORS"
        else
            print_warning "No GitHub Codespaces URL in CORS (may cause issues in Codespaces)"
        fi
    else
        print_status 1 "CORS_ORIGINS is not set"
    fi
else
    print_status 1 ".env file not found"
    echo "   Run: cp .env.example .env"
fi
echo ""

# Check backend health
echo "5. Checking backend API health..."
BACKEND_URLS=(
    "http://localhost:8000/health"
)

# If in Codespaces, add Codespace URL
if [ -n "$CODESPACE_NAME" ]; then
    BACKEND_URLS+=("https://${CODESPACE_NAME}-8000.app.github.dev/health")
fi

HEALTH_OK=0
for URL in "${BACKEND_URLS[@]}"; do
    if curl -sf "$URL" > /dev/null 2>&1; then
        print_status 0 "Backend is responding at $URL"
        HEALTH_OK=1
        break
    fi
done

if [ $HEALTH_OK -eq 0 ]; then
    print_status 1 "Backend is not responding"
    echo "   Tried URLs: ${BACKEND_URLS[*]}"
fi
echo ""

# Check database connectivity
echo "6. Checking database connectivity..."
if docker ps --filter "name=postgres" --format "{{.Names}}" | grep -q postgres; then
    if docker exec $(docker ps --filter "name=postgres" --format "{{.Names}}") psql -U taarez -d taarez_db -c "SELECT 1;" > /dev/null 2>&1; then
        print_status 0 "PostgreSQL is accessible"
        
        # Check if users exist
        USER_COUNT=$(docker exec $(docker ps --filter "name=postgres" --format "{{.Names}}") psql -U taarez -d taarez_db -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null || echo "0")
        USER_COUNT=$(echo $USER_COUNT | xargs)
        
        if [ "$USER_COUNT" != "0" ] && [ -n "$USER_COUNT" ]; then
            print_status 0 "Users table exists with $USER_COUNT users"
        else
            print_warning "Users table is empty or doesn't exist"
            echo "   Run: docker compose exec backend python create_test_users.py"
        fi
    else
        print_status 1 "PostgreSQL is not accessible"
    fi
else
    print_status 1 "PostgreSQL container is not running"
fi
echo ""

# Check Flutter configuration
echo "7. Checking Flutter configuration..."
FLUTTER_CONFIG="mobile-app/lib/utils/app_config.dart"
if [ -f "$FLUTTER_CONFIG" ]; then
    print_status 0 "Flutter config file exists"
    
    API_URL=$(grep "defaultValue:" "$FLUTTER_CONFIG" | grep -o "https://[^'\"]*" || echo "")
    if [ -n "$API_URL" ]; then
        echo "   API URL: $API_URL"
        
        if [[ $API_URL == *"github.dev"* ]]; then
            print_status 0 "Configured for GitHub Codespaces"
        elif [[ $API_URL == *"localhost"* ]]; then
            print_status 0 "Configured for local development"
        else
            print_warning "Unexpected API URL configuration"
        fi
    fi
else
    print_status 1 "Flutter config file not found"
fi
echo ""

# Check port availability
echo "8. Checking port availability..."
check_port() {
    if nc -z localhost $1 2>/dev/null; then
        print_status 0 "Port $1 is in use (expected)"
    else
        print_warning "Port $1 is not in use (service may not be running)"
    fi
}

check_port 8000  # Backend
check_port 5432  # PostgreSQL
echo ""

# Summary
echo "=================================="
echo "📊 Diagnostic Summary"
echo "=================================="
echo ""

if [ $HEALTH_OK -eq 1 ] && [ $BACKEND_RUNNING -eq 1 ] && [ $POSTGRES_RUNNING -eq 1 ]; then
    echo -e "${GREEN}✅ All critical services are operational${NC}"
    echo ""
    echo "You can now:"
    echo "  1. Access backend API: http://localhost:8000/docs"
    echo "  2. Login with: test@example.com / password123"
    echo ""
else
    echo -e "${RED}❌ Some services are not working properly${NC}"
    echo ""
    echo "Suggested actions:"
    echo "  1. Start services:    docker compose up -d"
    echo "  2. Check logs:        docker compose logs -f"
    echo "  3. Restart services:  docker compose restart"
    echo "  4. Reset everything:  docker compose down -v && docker compose up -d"
    echo ""
fi

# Additional help
echo "For more help, see:"
echo "  - CODESPACES-SETUP.md (for GitHub Codespaces)"
echo "  - QUICKSTART-INFRASTRUCTURE.md (for local setup)"
echo "  - docker compose logs (for detailed logs)"
