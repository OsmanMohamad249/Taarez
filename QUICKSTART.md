# Quick Start Guide - Sprint 1 Authentication System

Get up and running in 5 minutes!

## 1. Prerequisites Check

```bash
# Check Docker
docker --version

# Check Flutter
flutter --version
```

If missing:
- Install Docker: https://docs.docker.com/get-docker/
- Install Flutter: https://docs.flutter.dev/get-started/install

## 2. Start Backend (2 minutes)

```bash
# From project root
docker-compose up --build
```

Wait for: `Application startup complete`

In a **new terminal**:

```bash
# Run database migrations
docker-compose exec backend bash
cd /app && alembic upgrade head && exit
```

✅ Backend is ready at http://localhost:8000/docs

## 3. Start Mobile App (2 minutes)

```bash
cd mobile-app
flutter pub get
flutter run
```

Select your device when prompted.

✅ App should launch and show splash screen

## 4. Test Authentication (1 minute)

### In the Mobile App:

1. Click "Don't have an account? Register"
2. Enter:
   - Email: `demo@test.com`
   - Password: `demo123`
3. Click "Register"
4. See success message
5. Click "Already have an account? Login"
6. Login with same credentials
7. See Home screen with your email

### Test Persistence:

1. Close the app completely
2. Reopen the app
3. You should see Home screen (auto-login)

### Test Logout:

1. Click "Logout" button
2. You're back at Login screen
3. Token is cleared

## 5. Verify API (30 seconds)

```bash
# Test registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"api@test.com","password":"test123"}'

# Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=api@test.com&password=test123"
```

## Troubleshooting

### Backend issues?
- Check: `docker-compose ps` (both services should be "Up")
- Logs: `docker-compose logs backend`

### Mobile app connection error?
- Android Emulator: URL should be `http://10.0.2.2:8000`
- Physical device: Update URL in `lib/services/auth_service.dart` to your computer's IP

### Migration error?
```bash
docker-compose down -v
docker-compose up --build
# Then run migrations again
```

## What's Next?

- See **SPRINT1_SETUP_GUIDE.md** for detailed setup
- See **SPRINT1_SUMMARY.md** for implementation details
- Run tests: `cd backend && pytest tests/`

## Common Commands

```bash
# Stop services
docker-compose down

# View database
docker-compose exec postgres psql -U tiraz -d tiraz_db
\dt
SELECT * FROM users;
\q

# Backend logs
docker-compose logs -f backend

# Reset database
docker-compose down -v
docker-compose up
```

🎉 **You're all set!** The authentication system is fully functional.
