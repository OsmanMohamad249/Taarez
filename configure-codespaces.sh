#!/bin/bash
# Script to configure Taarez for GitHub Codespaces
# This script automatically updates CORS and Flutter configuration with Codespace URLs

set -e

echo "🔧 Configuring Taarez for GitHub Codespaces..."
echo ""

# Function to detect if we're in a Codespace
is_codespace() {
    [ -n "$CODESPACE_NAME" ]
}

# Check if running in Codespaces
if ! is_codespace; then
    echo "⚠️  Warning: This script is designed for GitHub Codespaces"
    echo "   It will still run, but you may need to manually configure URLs"
    echo ""
fi

# Get Codespace URL if available
if is_codespace; then
    CODESPACE_URL="https://${CODESPACE_NAME}-8000.app.github.dev"
    FLUTTER_URL="https://${CODESPACE_NAME}-8080.app.github.dev"
    echo "✅ Detected Codespace URLs:"
    echo "   Backend:  $CODESPACE_URL"
    echo "   Frontend: $FLUTTER_URL"
    echo ""
else
    echo "📝 Enter your Codespace backend URL (e.g., https://xxx-8000.app.github.dev):"
    read -p "Backend URL: " CODESPACE_URL
    echo ""
    echo "📝 Enter your Codespace frontend URL (e.g., https://xxx-8080.app.github.dev):"
    read -p "Frontend URL: " FLUTTER_URL
    echo ""
fi

# Update .env file
echo "📝 Updating .env file..."
if [ -f .env ]; then
    # Check if CORS_ORIGINS already has a github.dev URL
    if grep -q "github.dev" .env; then
        echo "   ℹ️  .env already has a github.dev URL"
        echo "   ℹ️  CORS regex pattern will allow all Codespace URLs"
    else
        # Add the Flutter URL to CORS_ORIGINS
        sed -i.bak "s|CORS_ORIGINS=.*|CORS_ORIGINS=http://localhost:3000,http://localhost:8080,${FLUTTER_URL}|" .env
        echo "   ✅ Updated CORS_ORIGINS in .env"
    fi
else
    echo "   ⚠️  .env file not found"
fi

# Update Flutter configuration
echo "📝 Updating Flutter app configuration..."
FLUTTER_CONFIG="mobile-app/lib/utils/app_config.dart"
if [ -f "$FLUTTER_CONFIG" ]; then
    # Update the apiBaseUrl default value
    sed -i.bak "s|defaultValue: '.*'|defaultValue: '${CODESPACE_URL}'|" "$FLUTTER_CONFIG"
    echo "   ✅ Updated $FLUTTER_CONFIG"
else
    echo "   ⚠️  $FLUTTER_CONFIG not found"
fi

echo ""
echo "🎯 Configuration complete!"
echo ""
echo "Next steps:"
echo "1. Restart backend:    docker compose restart backend"
echo "2. Rebuild Flutter:    cd mobile-app && flutter build web"
echo "3. Access frontend:    $FLUTTER_URL"
echo ""
echo "Test credentials:"
echo "  Email:    test@example.com"
echo "  Password: password123"
echo ""
echo "📝 Remember to set ports 8000 and 8080 to 'Public' in the PORTS tab!"
