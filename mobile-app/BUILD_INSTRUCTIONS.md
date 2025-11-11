# Flutter Mobile App - Build Instructions

## Running in Docker

The Flutter mobile app can be run in Docker using the flutter-dev service:

```bash
# Build the Docker image
docker compose build flutter-dev

# Run the Flutter app on web server (port 8080)
docker compose up flutter-dev
```

The app will be available at http://localhost:8080

## Local Development

If you have Flutter installed locally, you can run:

```bash
cd mobile-app
flutter pub get
flutter run -d web-server --web-port 8080 --web-hostname 0.0.0.0
```

## Environment Configuration

The app uses `AppConfig` to determine the API base URL:

- **Docker environment**: `http://backend:8000` (default)
- **Android Emulator**: `http://10.0.2.2:8000`
- **iOS Simulator**: `http://localhost:8000`

To override the default URL, set the `API_BASE_URL` environment variable when running:

```bash
flutter run -d web-server --dart-define=API_BASE_URL=http://your-backend:8000
```

## Authentication Flow

The app implements a complete authentication flow:

1. **Splash Screen**: Checks if user is authenticated on app start
2. **Login Screen**: Allows users to log in with email/password
3. **Home Screen**: Displays user information and logout button

All authentication state is managed using Riverpod with custom union-type state classes.

## Architecture

The app follows a feature-based architecture:

```
lib/
├── features/
│   └── auth/
│       ├── domain/          # State classes (auth_state.dart)
│       └── presentation/    # Providers and UI (screens)
├── models/                  # Data models (User, etc.)
├── services/               # API services (auth_service, api_service)
└── utils/                  # Configuration and helpers
```

## State Management

The authentication state uses a custom union-type implementation that mimics freezed's functionality:

- `AuthStateInitial`: Initial state
- `AuthStateLoading`: Loading state
- `AuthStateAuthenticated`: User is logged in
- `AuthStateUnauthenticated`: User is not logged in
- `AuthStateError`: Error occurred

These states support pattern matching via `when()`, `whenOrNull()`, and `maybeWhen()` methods.
