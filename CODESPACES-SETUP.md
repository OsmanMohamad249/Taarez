# 🔧 GitHub Codespaces Configuration for Taarez

## Overview
This guide explains how to run Taarez in GitHub Codespaces with proper authentication and networking.

## 🚀 Quick Start in Codespaces

### 1. Start the Application
```bash
# Make sure you're in the project root
cd /workspaces/Taarez

# Start all services with Docker Compose
docker compose up -d
```

### 2. Wait for Services to Initialize
```bash
# Watch the logs to see when services are ready
docker compose logs -f backend

# You should see:
# - "PostgreSQL is ready!"
# - "Running database migrations..."
# - "Creating test users (if needed)..."
# - "Starting FastAPI application on port 8000..."
```

### 3. Configure Port Visibility
In GitHub Codespaces, you need to make ports public:
1. Go to the **PORTS** tab in VS Code
2. Find port **8000** (Backend API)
3. Right-click and select **Port Visibility** → **Public**
4. Find port **8080** (Flutter Web App)
5. Right-click and select **Port Visibility** → **Public**

### 4. Update CORS Configuration
The backend needs to know which Codespaces URLs to allow. Update `.env`:

```bash
# Find your Codespace URL from the PORTS tab
# It will look like: https://xxx-8080.app.github.dev

# Update .env CORS_ORIGINS to include your Codespace URLs
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://YOUR-CODESPACE-8080.app.github.dev
```

**Or use the auto-regex pattern** (already configured):
- If any `github.dev` URL is in CORS_ORIGINS, the backend will automatically allow all `*.app.github.dev` URLs

### 5. Update Flutter App Configuration
Update `mobile-app/lib/utils/app_config.dart`:

```dart
static const String apiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'https://YOUR-CODESPACE-8000.app.github.dev',
);
```

Replace `YOUR-CODESPACE-8000.app.github.dev` with your actual Codespace URL from the PORTS tab.

### 6. Rebuild Flutter App
```bash
cd mobile-app
flutter pub get
flutter build web
cd ..
```

### 7. Access the Application
- **Backend API**: `https://YOUR-CODESPACE-8000.app.github.dev`
- **API Docs**: `https://YOUR-CODESPACE-8000.app.github.dev/docs`
- **Flutter Web App**: `https://YOUR-CODESPACE-8080.app.github.dev`

## 🔐 Test Credentials

The application automatically creates these test users:

| Email | Password | Role |
|-------|----------|------|
| test@example.com | password123 | Customer |
| designer@example.com | password123 | Designer |
| admin@example.com | password123 | Admin |

## 🐛 Troubleshooting

### Issue: "Network error: XMLHttpRequest error"

**Cause**: CORS configuration not allowing Codespaces URLs

**Solution**:
1. Check that `.env` has a `github.dev` URL in `CORS_ORIGINS`
2. Restart backend: `docker compose restart backend`
3. Verify CORS in browser DevTools → Network tab → Response Headers

### Issue: "HTTP 401 Unauthorized" or "www-authenticate: tunnel"

**Cause**: Port is not set to Public visibility

**Solution**:
1. Open PORTS tab in VS Code
2. Right-click port 8000 → Port Visibility → Public
3. Right-click port 8080 → Port Visibility → Public

### Issue: Backend returns 500 "Internal Server Error"

**Cause**: Might be the bcrypt password length issue or database connection

**Solution**:
1. Check backend logs: `docker compose logs backend`
2. Look for "ValueError: password cannot be longer than 72 bytes"
3. Ensure password is <= 72 characters (already enforced in schemas)

### Issue: "This page isn't working" / HTTP ERROR 502

**Cause**: Backend or Flutter service not running

**Solution**:
```bash
# Check service status
docker compose ps

# Restart services
docker compose restart

# View logs for errors
docker compose logs backend
docker compose logs flutter-dev
```

### Issue: Database connection errors

**Cause**: PostgreSQL not ready or wrong credentials

**Solution**:
```bash
# Check PostgreSQL is running
docker compose ps postgres

# Restart database
docker compose restart postgres

# Check database connectivity
docker compose exec postgres psql -U taarez -d taarez_db -c "SELECT 1;"
```

### Issue: Test users not created

**Cause**: Migration or user creation script failed

**Solution**:
```bash
# Manually create test users
docker compose exec backend python create_test_users.py

# Or recreate the database
docker compose down -v
docker compose up -d
```

## 🔍 Verification Steps

### 1. Backend Health Check
```bash
curl https://YOUR-CODESPACE-8000.app.github.dev/health
# Expected: {"status":"ok","service":"taarez-backend"}
```

### 2. API Documentation
Visit: `https://YOUR-CODESPACE-8000.app.github.dev/docs`
Should see FastAPI Swagger UI

### 3. Test Login via API
```bash
curl -X POST "https://YOUR-CODESPACE-8000.app.github.dev/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# Expected: {"access_token":"...","token_type":"bearer"}
```

### 4. Test Flutter App Login
1. Open: `https://YOUR-CODESPACE-8080.app.github.dev`
2. Enter: `test@example.com` / `password123`
3. Should successfully log in and see dashboard

## 📝 Key Configuration Files

### Backend Configuration
- **`.env`**: Environment variables (SECRET_KEY, DATABASE_URL, CORS_ORIGINS)
- **`backend/core/config.py`**: Configuration class
- **`backend/main.py`**: CORS middleware with regex pattern support
- **`backend/core/security.py`**: Password hashing with 72-byte validation

### Frontend Configuration
- **`mobile-app/lib/utils/app_config.dart`**: API base URL
- **`mobile-app/lib/services/auth_service.dart`**: Authentication service

### Docker Configuration
- **`docker-compose.yml`**: Service definitions
- **`backend/Dockerfile`**: Backend container
- **`backend/entrypoint.sh`**: Startup script with auto-migrations and test user creation

## 🎯 Architecture

```
┌─────────────────────────────────────────────────────┐
│         GitHub Codespaces Environment                │
│                                                      │
│  ┌──────────────┐      ┌──────────────┐            │
│  │ Flutter Web  │─────→│  Backend API │            │
│  │   (8080)     │ CORS │   (8000)     │            │
│  └──────────────┘      └───────┬──────┘            │
│                                 │                    │
│                        ┌────────▼──────┐            │
│                        │  PostgreSQL   │            │
│                        │    (5432)     │            │
│                        └───────────────┘            │
└─────────────────────────────────────────────────────┘
```

## 🔒 Security Notes

1. **SECRET_KEY**: Already set in `.env` (FOOwBOjh8aUt63LzPVtofmxPFX0kIhB1mdYhzdVWf_4)
2. **CORS**: Uses regex pattern to allow all Codespaces URLs
3. **Passwords**: Limited to 72 bytes (bcrypt requirement)
4. **Test Users**: Only for development, disable in production

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flutter Documentation](https://flutter.dev/docs)
- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## ✅ Success Criteria

When everything is working:
- ✅ Backend API responds at `/health`
- ✅ API docs visible at `/docs`
- ✅ Flutter web app loads
- ✅ Can login with test@example.com
- ✅ No CORS errors in browser console
- ✅ No 502/401 errors

---

**Last Updated**: 2025-11-11
**Status**: Ready for GitHub Codespaces ✅
