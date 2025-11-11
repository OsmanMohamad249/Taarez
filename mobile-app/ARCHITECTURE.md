# Flutter Mobile App Architecture

## Before → After Restructuring

### Before (Old Structure)
```
mobile-app/lib/
├── main.dart
├── models/
│   └── user.dart
├── providers/
│   └── auth_provider.dart           # Old flat provider
├── screens/
│   └── auth/
│       ├── splash_screen.dart
│       ├── login_screen.dart
│       └── home_screen.dart
├── services/
│   ├── api_service.dart
│   └── auth_service.dart
└── utils/
    └── app_config.dart
```

**Issues**:
- No clear feature separation
- State management mixed with UI
- No standardized state pattern
- Backend URL hardcoded for Android emulator

### After (New Feature-Based Structure)
```
mobile-app/lib/
├── main.dart                         # Entry point
├── features/
│   └── auth/                         # ✨ NEW: Auth feature module
│       ├── domain/
│       │   └── auth_state.dart       # ✨ NEW: Union-type states
│       └── presentation/
│           ├── auth_provider.dart    # ✨ UPDATED: Riverpod provider
│           ├── splash_screen.dart    # ✨ UPDATED: Auto-navigation
│           ├── login_screen.dart     # ✨ UPDATED: New state handling
│           └── home_screen.dart      # ✨ UPDATED: Reactive UI
├── models/
│   └── user.dart                     # Unchanged
├── services/
│   ├── api_service.dart              # Unchanged
│   └── auth_service.dart             # Unchanged
└── utils/
    └── app_config.dart               # ✨ UPDATED: Docker backend URL
```

**Improvements**:
- ✅ Clear feature-based organization
- ✅ Separation of domain and presentation
- ✅ Type-safe state management
- ✅ Docker-compatible configuration

## Authentication Flow

### State Transitions

```
┌─────────────────┐
│  App Startup    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AuthStateInitial│
└────────┬────────┘
         │
         │ checkAuth()
         ▼
┌─────────────────┐
│ AuthStateLoading│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌───────────────────┐
│  Token  │ │   Token Exists    │
│ Missing │ │  & User Fetched   │
└────┬────┘ └─────────┬─────────┘
     │                │
     ▼                ▼
┌──────────────────┐ ┌────────────────────┐
│AuthStateUnauthen-│ │AuthStateAuthentica-│
│     ticated      │ │       ted          │
└──────────────────┘ └────────────────────┘
         │                     │
         │                     │
         ▼                     ▼
   ┌──────────┐         ┌──────────┐
   │  Login   │         │   Home   │
   │  Screen  │         │  Screen  │
   └──────────┘         └──────────┘
```

### User Journey

```
┌───────────────────────────────────────────────────────┐
│ 1. App Launch                                         │
│    ↓                                                   │
│    Splash Screen shows                                │
│    checkAuth() called                                 │
└───────────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
┌──────────────┐            ┌──────────────┐
│ No Token     │            │ Token Found  │
│ Found        │            │              │
└──────┬───────┘            └──────┬───────┘
       │                           │
       ▼                           ▼
┌──────────────┐            ┌──────────────┐
│ 2. Login     │            │ 2. Fetch User│
│    Screen    │            │    Data      │
│              │            └──────┬───────┘
│ - Email      │                   │
│ - Password   │              ┌────┴────┐
│ - Validate   │              │         │
│ - Submit     │              ▼         ▼
└──────┬───────┘         ┌────────┐ ┌────────┐
       │                 │Success │ │ Failed │
       │                 └────┬───┘ └───┬────┘
       │                      │         │
       ▼                      │         │
┌──────────────┐              │    ┌────┴──────┐
│ login() API  │              │    │ Redirect  │
└──────┬───────┘              │    │ to Login  │
       │                      │    └───────────┘
  ┌────┴────┐                 │
  │         │                 │
  ▼         ▼                 │
┌──────┐ ┌──────┐            │
│Error │ │Token │            │
│      │ │Saved │            │
└──┬───┘ └───┬──┘            │
   │         │               │
   │         └───────┬───────┘
   │                 │
   ▼                 ▼
┌─────────┐   ┌──────────────────┐
│ Show    │   │ 3. Home Screen   │
│ Error   │   │                  │
└─────────┘   │ - Display User   │
              │ - Logout Button  │
              └──────────────────┘
                       │
                  logout()
                       │
                       ▼
              ┌──────────────────┐
              │ Clear Token      │
              │ → Login Screen   │
              └──────────────────┘
```

## State Management Pattern

### AuthState Union Type

```dart
// Base class with pattern matching
abstract class AuthState {
  T when<T>({
    required T Function() initial,
    required T Function() loading,
    required T Function(User user) authenticated,
    required T Function() unauthenticated,
    required T Function(String message) error,
  });
}

// Concrete states
class AuthStateInitial extends AuthState { ... }
class AuthStateLoading extends AuthState { ... }
class AuthStateAuthenticated extends AuthState {
  final User user;
}
class AuthStateUnauthenticated extends AuthState { ... }
class AuthStateError extends AuthState {
  final String message;
}
```

### Usage Example

```dart
// In UI components
authState.when(
  initial: () => CircularProgressIndicator(),
  loading: () => CircularProgressIndicator(),
  authenticated: (user) => HomeScreen(user: user),
  unauthenticated: () => LoginScreen(),
  error: (message) => ErrorWidget(message: message),
);
```

## Component Communication

```
┌─────────────────────────────────────────────────┐
│                   UI Layer                       │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Splash    │  │  Login   │  │   Home     │  │
│  │  Screen    │  │  Screen  │  │   Screen   │  │
│  └─────┬──────┘  └─────┬────┘  └─────┬──────┘  │
└────────┼───────────────┼─────────────┼──────────┘
         │               │             │
         └───────┬───────┴─────┬───────┘
                 │             │
         ┌───────▼─────────────▼───────┐
         │     AuthStateProvider       │
         │    (Riverpod Provider)      │
         └───────────┬─────────────────┘
                     │
         ┌───────────▼─────────────────┐
         │    AuthStateNotifier        │
         │  ┌─────────────────────┐    │
         │  │ - checkAuth()       │    │
         │  │ - login()           │    │
         │  │ - logout()          │    │
         │  └─────────────────────┘    │
         └───────────┬─────────────────┘
                     │
         ┌───────────▼─────────────────┐
         │      AuthService            │
         │  ┌─────────────────────┐    │
         │  │ - HTTP requests     │    │
         │  │ - Token storage     │    │
         │  │ - User fetch        │    │
         │  └─────────────────────┘    │
         └───────────┬─────────────────┘
                     │
         ┌───────────▼─────────────────┐
         │  Backend API (FastAPI)      │
         │  http://backend:8000        │
         │  ┌─────────────────────┐    │
         │  │ POST /auth/login    │    │
         │  │ GET  /users/me      │    │
         │  └─────────────────────┘    │
         └─────────────────────────────┘
```

## Security Architecture

```
┌────────────────────────────────────────────┐
│         User Credentials                   │
│     (Email + Password)                     │
└───────────────┬────────────────────────────┘
                │ HTTPS
                ▼
┌────────────────────────────────────────────┐
│         Backend Authentication             │
│         POST /api/v1/auth/login           │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│         JWT Token Generated                │
│         (access_token)                     │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│    flutter_secure_storage                  │
│    (Encrypted Storage)                     │
│    ┌────────────────────────────────┐     │
│    │  Key: "access_token"           │     │
│    │  Value: "eyJ0eXAi..."          │     │
│    └────────────────────────────────┘     │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│   Subsequent API Requests                  │
│   Header: "Authorization: Bearer <token>"  │
└────────────────────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│   Backend Validates Token                  │
│   ✓ Signature Valid                        │
│   ✓ Not Expired                            │
│   ✓ User Exists                            │
└────────────────────────────────────────────┘
```

## Docker Network Configuration

```
┌─────────────────────────────────────────────────┐
│              Docker Network                      │
│                                                  │
│  ┌──────────────────┐    ┌──────────────────┐  │
│  │  flutter-dev     │    │     backend      │  │
│  │  Port: 8080      │───▶│  Port: 8000     │  │
│  │                  │    │                  │  │
│  │  API URL:        │    │  FastAPI Server  │  │
│  │  http://backend: │    │                  │  │
│  │        8000      │    │                  │  │
│  └──────────────────┘    └────────┬─────────┘  │
│                                    │             │
│                            ┌───────▼─────────┐  │
│                            │    postgres     │  │
│                            │  Port: 5432     │  │
│                            │                 │  │
│                            │  Database:      │  │
│                            │  tiraz_db       │  │
│                            └─────────────────┘  │
└─────────────────────────────────────────────────┘
         │                           │
         │ Port Mapping              │ Port Mapping
         ▼                           ▼
   localhost:8080              localhost:8000
   (Flutter Web)               (API Endpoints)
```

## Technology Stack

```
┌────────────────────────────────────────────┐
│           Frontend (Flutter)               │
│  ┌──────────────────────────────────┐     │
│  │ UI Framework: Flutter 3.7.7      │     │
│  │ Language: Dart                   │     │
│  │ State Management: Riverpod       │     │
│  │ HTTP Client: http package        │     │
│  │ Secure Storage: flutter_secure   │     │
│  └──────────────────────────────────┘     │
└────────────────────────────────────────────┘
                    │
                    │ HTTP/HTTPS
                    ▼
┌────────────────────────────────────────────┐
│           Backend (FastAPI)                │
│  ┌──────────────────────────────────┐     │
│  │ Framework: FastAPI                │     │
│  │ Language: Python 3.11             │     │
│  │ Auth: JWT (python-jose)           │     │
│  │ Database ORM: SQLAlchemy          │     │
│  └──────────────────────────────────┘     │
└────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────┐
│          Database (PostgreSQL)             │
│  ┌──────────────────────────────────┐     │
│  │ Version: PostgreSQL 15            │     │
│  │ Migrations: Alembic               │     │
│  │ Tables: users, designs, etc.      │     │
│  └──────────────────────────────────┘     │
└────────────────────────────────────────────┘
```

## Key Benefits of New Architecture

1. **Scalability**: Easy to add new features
2. **Maintainability**: Clear separation of concerns
3. **Testability**: Each layer can be tested independently
4. **Type Safety**: Compile-time guarantees
5. **Security**: Proper token management
6. **Developer Experience**: Clean, readable code
