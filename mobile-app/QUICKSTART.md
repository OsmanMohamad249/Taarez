# Quick Start Guide - Flutter Mobile App

## 🚀 Quick Commands

```bash
# Start backend services
docker compose up -d backend postgres

# Build Flutter app
docker compose build flutter-dev

# Run Flutter app
docker compose up flutter-dev

# View logs
docker compose logs -f flutter-dev

# Stop services
docker compose down
```

## 📂 Project Structure

```
mobile-app/
├── lib/
│   ├── features/auth/          # ✨ NEW authentication feature
│   │   ├── domain/             # State definitions
│   │   └── presentation/       # UI & providers
│   ├── models/                 # Data models
│   ├── services/               # API services
│   └── utils/                  # Utilities
├── ARCHITECTURE.md             # System architecture diagrams
├── IMPLEMENTATION_SUMMARY.md   # What was done
├── BUILD_INSTRUCTIONS.md       # How to build
└── TESTING_GUIDE.md           # How to test
```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `lib/features/auth/domain/auth_state.dart` | Auth state definitions (5 states) |
| `lib/features/auth/presentation/auth_provider.dart` | State management logic |
| `lib/features/auth/presentation/splash_screen.dart` | Initial auth check screen |
| `lib/features/auth/presentation/login_screen.dart` | Login UI |
| `lib/features/auth/presentation/home_screen.dart` | Authenticated home |
| `lib/utils/app_config.dart` | Backend URL configuration |
| `lib/services/auth_service.dart` | API calls for auth |

## 🔧 Configuration

### Backend URL
Default: `http://backend:8000` (Docker)

Override with environment variable:
```bash
flutter run --dart-define=API_BASE_URL=http://your-backend:8000
```

### Environment Variables (.env)
```bash
SECRET_KEY=<strong-secret-key>
DATABASE_URL=postgresql://tiraz:tiraz_password@postgres:5432/tiraz_db
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🎯 Authentication States

```dart
AuthStateInitial       // Initial state
AuthStateLoading       // Processing
AuthStateAuthenticated // Logged in (has User)
AuthStateUnauthenticated // Not logged in
AuthStateError         // Error (has message)
```

## 📖 Usage Examples

### Check Auth State
```dart
final authState = ref.watch(authStateProvider);

authState.when(
  initial: () => CircularProgressIndicator(),
  loading: () => CircularProgressIndicator(),
  authenticated: (user) => Text('Hello ${user.displayName}'),
  unauthenticated: () => LoginButton(),
  error: (message) => Text('Error: $message'),
);
```

### Login
```dart
final success = await ref.read(authStateProvider.notifier).login(
  email,
  password,
);
```

### Logout
```dart
await ref.read(authStateProvider.notifier).logout();
```

### Check Auth on Startup
```dart
await ref.read(authStateProvider.notifier).checkAuth();
```

## 🔐 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/auth/login` | Login with credentials |
| POST | `/api/v1/auth/register` | Register new user |
| GET | `/api/v1/users/me` | Get current user info |

## 🧪 Testing

### Manual Testing Flow
1. Start backend: `docker compose up -d backend postgres`
2. Open browser: `http://localhost:8080`
3. Try login (or register first)
4. Verify home screen shows user data
5. Test logout

### Test Credentials
Register via API or use existing test user:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

## 🐛 Troubleshooting

### Issue: "Failed to download Web SDK"
**Cause**: Network restrictions  
**Solution**: Deploy to environment with internet access or pre-download SDK

### Issue: "Backend connection refused"
**Cause**: Backend not running  
**Solution**: `docker compose up -d backend postgres`

### Issue: "401 Unauthorized"
**Cause**: Token expired or invalid  
**Solution**: Logout and login again

### Issue: "flutter pub get fails"
**Cause**: Network restrictions  
**Solution**: Run in Docker container or with VPN

## 📚 Documentation

- **ARCHITECTURE.md**: Visual system diagrams
- **IMPLEMENTATION_SUMMARY.md**: Detailed implementation report
- **BUILD_INSTRUCTIONS.md**: Build and deployment guide
- **TESTING_GUIDE.md**: Testing procedures

## 🛠️ Development Tips

1. **Hot Reload**: Use `flutter run` for development (not in Docker)
2. **Debugging**: Use Chrome DevTools for web debugging
3. **State Inspection**: Use Riverpod DevTools for state debugging
4. **API Testing**: Use Postman or curl for backend testing

## ⚡ Performance Tips

1. Use const constructors where possible
2. Avoid unnecessary widget rebuilds
3. Implement proper error boundaries
4. Use secure storage for sensitive data
5. Cache API responses when appropriate

## 🔒 Security Checklist

- [x] Tokens stored in encrypted storage
- [x] HTTPS ready (backend supports)
- [x] No hardcoded secrets
- [x] Environment-based config
- [x] Proper token cleanup on logout
- [x] Input validation on forms
- [x] Error messages don't leak sensitive info

## 🎉 Next Steps

1. Resolve network restrictions or deploy to proper environment
2. Run full E2E tests
3. Add unit tests for business logic
4. Add widget tests for UI components
5. Set up CI/CD pipeline
6. Performance optimization
7. Accessibility improvements
8. Internationalization (i18n)

---

**Need Help?**
- Check `ARCHITECTURE.md` for system overview
- Check `TESTING_GUIDE.md` for testing procedures
- Check `IMPLEMENTATION_SUMMARY.md` for what was implemented
