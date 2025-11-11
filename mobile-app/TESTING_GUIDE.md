# Flutter Mobile App Testing Guide

## Current Status

The Flutter mobile app has been successfully refactored with the following improvements:

### ✅ Completed
1. **Restructured file organization** - Feature-based architecture with auth under `lib/features/auth/`
2. **Updated dependencies** - Removed freezed dependencies due to network restrictions
3. **Implemented union-type state management** - Manual implementation of union types for AuthState
4. **Fixed backend API connection** - Updated AppConfig to use `http://backend:8000` for Docker
5. **Updated UI screens** - Splash, Login, and Home screens use the new AuthProvider
6. **Backend is running** - FastAPI backend is operational on port 8000

### ⚠️ Known Limitations

Due to network restrictions in the build environment:
- Cannot download Flutter Web SDK from storage.googleapis.com (403 error)
- The `flutter build web` and `flutter run -d web-server` commands require downloading additional SDKs

## Testing Alternatives

### Option 1: Local Flutter Installation

If you have Flutter installed locally:

```bash
cd mobile-app
flutter pub get
flutter run -d web-server --web-port 8080
```

Then navigate to http://localhost:8080

### Option 2: Use a Different Docker Image

Use a Docker image that has the Web SDK pre-installed:

```dockerfile
FROM ghcr.io/cirruslabs/flutter:stable
# This image should have web SDK pre-installed
```

### Option 3: Manual Web SDK Installation

Inside the Docker container:

```bash
# Download web SDK manually (if network allows)
cd /sdks/flutter
flutter config --enable-web
flutter precache --web
```

## Expected Behavior

When the app runs successfully, you should see:

1. **Splash Screen** (initial load)
   - Shows "Tiraz" logo and loading indicator
   - Automatically checks authentication status
   - Redirects to Login or Home based on auth state

2. **Login Screen** (if not authenticated)
   - Email and password input fields
   - Login button
   - Link to registration

3. **Home Screen** (if authenticated)
   - Welcome message
   - User's display name and email
   - Logout button

## Testing Authentication Flow

To test the complete flow:

1. Start the backend: `docker compose up -d backend postgres`
2. Register a user via backend API or mobile app
3. Login with credentials
4. Verify user data is displayed
5. Test logout functionality

## API Endpoints

The backend provides these endpoints:

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `GET /api/v1/users/me` - Get current user info

## Code Structure

```
lib/
├── features/
│   └── auth/
│       ├── domain/
│       │   └── auth_state.dart          # Union-type auth states
│       └── presentation/
│           ├── auth_provider.dart       # Riverpod state notifier
│           ├── splash_screen.dart       # Initial screen with auth check
│           ├── login_screen.dart        # Login UI
│           └── home_screen.dart         # Authenticated home
├── models/
│   └── user.dart                         # User model
├── services/
│   ├── api_service.dart                  # Base API service
│   └── auth_service.dart                 # Auth API calls
└── utils/
    └── app_config.dart                   # Environment configuration
```

## Security Notes

- Uses `flutter_secure_storage` for token persistence
- JWT tokens are sent with `Bearer` authentication
- Backend validates tokens on protected routes
- Tokens are cleared on logout

## Next Steps

To complete testing:

1. Resolve network restrictions or use a different environment
2. Pre-download the Flutter Web SDK
3. Test complete authentication flow
4. Test error handling (wrong credentials, network errors)
5. Test state persistence across app restarts
