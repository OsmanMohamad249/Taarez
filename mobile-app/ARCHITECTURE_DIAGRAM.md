# Designer Dashboard Architecture Diagram

## Component Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         AUTHENTICATION                           │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │ SplashScreen │ ───> │ LoginScreen  │ ───> │   Backend    │  │
│  │  (Check Auth)│      │ (Get Token)  │      │  /auth/login │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│         │                     │                      │           │
│         │                     │                      │           │
│         └─────────────────────┴──────────────────────┘           │
│                               │                                  │
│                   ┌───────────▼───────────┐                      │
│                   │   AuthStateProvider   │                      │
│                   │   (Riverpod State)    │                      │
│                   │   - User with Role    │                      │
│                   └───────────┬───────────┘                      │
│                               │                                  │
│                    ┌──────────▼──────────┐                       │
│                    │   Role Check        │                       │
│                    └──────────┬──────────┘                       │
│                               │                                  │
│              ┌────────────────┴────────────────┐                 │
│              │                                 │                 │
│              ▼                                 ▼                 │
│      ┌────────────────┐              ┌────────────────┐          │
│      │  role: designer│              │role: customer  │          │
│      └────────────────┘              └────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
              │                                 │
              │                                 │
              ▼                                 ▼
┌───────────────────────────┐      ┌──────────────────────────┐
│  DesignerDashboardScreen  │      │     HomeScreen           │
│  (Designer's Hub)         │      │     (Customer UI)        │
└───────────────────────────┘      └──────────────────────────┘
              │
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DESIGNER DASHBOARD                           │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                     AppBar                             │     │
│  │  [My Designs]              [Refresh] [Logout]          │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │              myDesignsProvider (Riverpod)              │     │
│  │                  (FutureProvider)                      │     │
│  └──────────────────────┬─────────────────────────────────┘     │
│                         │                                        │
│           ┌─────────────┼─────────────┐                          │
│           │             │             │                          │
│           ▼             ▼             ▼                          │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│    │ Loading  │  │   Data   │  │  Error   │                     │
│    │  State   │  │  State   │  │  State   │                     │
│    └──────────┘  └──────────┘  └──────────┘                     │
│         │             │             │                            │
│         ▼             ▼             ▼                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │ Spinner  │  │ListView  │  │Error Msg │                       │
│  │          │  │ of       │  │+ Retry   │                       │
│  │          │  │Designs   │  │Button    │                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
│                     │                                            │
│              ┌──────┴──────┐                                     │
│              │             │                                     │
│         Empty State?   Has Designs?                              │
│              │             │                                     │
│              ▼             ▼                                     │
│      ┌────────────┐  ┌──────────────┐                           │
│      │ "No designs│  │DesignListItem│                           │
│      │  yet"      │  │   (Cards)    │                           │
│      │ + Help Text│  │              │                           │
│      └────────────┘  └──────────────┘                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │           FloatingActionButton [+]                     │     │
│  └────────────────────┬───────────────────────────────────┘     │
│                       │                                          │
└───────────────────────┼──────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ADD DESIGN SCREEN                             │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                     AppBar                             │     │
│  │              [Add New Design]                          │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                  Form (with validation)                │     │
│  │  ┌──────────────────────────────────────────────┐      │     │
│  │  │  Design Name *                                │      │     │
│  │  │  [                            ]               │      │     │
│  │  └──────────────────────────────────────────────┘      │     │
│  │  ┌──────────────────────────────────────────────┐      │     │
│  │  │  Description *                                │      │     │
│  │  │  [                            ]               │      │     │
│  │  │  [                            ]               │      │     │
│  │  └──────────────────────────────────────────────┘      │     │
│  │  ┌──────────────────────────────────────────────┐      │     │
│  │  │  Base Price (SAR) *                           │      │     │
│  │  │  [                            ]               │      │     │
│  │  └──────────────────────────────────────────────┘      │     │
│  │                                                         │     │
│  │  ┌──────────────────────────────────────────────┐      │     │
│  │  │         [Save Design]                         │      │     │
│  │  └──────────────────────────────────────────────┘      │     │
│  └────────────────────────────────────────────────────────┘     │
│                         │                                        │
│                         │ (on success)                           │
│                         ▼                                        │
│              ┌─────────────────────┐                             │
│              │  DesignService      │                             │
│              │  .createDesign()    │                             │
│              └──────────┬──────────┘                             │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────┐                             │
│              │ POST /designs/      │                             │
│              │ (Backend API)       │                             │
│              └──────────┬──────────┘                             │
│                         │                                        │
│                         ▼                                        │
│              ┌─────────────────────┐                             │
│              │ Success SnackBar    │                             │
│              │ Pop to Dashboard    │                             │
│              │ Refresh List        │                             │
│              └─────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘


## Data Flow

1. **Authentication Flow**
   - User enters credentials → AuthService.login()
   - Token stored securely → AuthService.getCurrentUser()
   - User profile with role fetched
   - Role checked: designer vs customer

2. **Designer Dashboard Flow**
   - myDesignsProvider triggered
   - DesignService.getMyDesigns()
   - GET /designs/me with Bearer token
   - Backend validates role
   - Returns list of designs
   - UI updates based on state

3. **Create Design Flow**
   - User fills form
   - Validation runs
   - DesignService.createDesign()
   - POST /designs/ with data
   - Backend creates design
   - Success → Pop to dashboard
   - Dashboard auto-refreshes

## State Management

```
Riverpod Providers
├── authStateProvider (StateNotifier)
│   ├── User model with role
│   ├── isAuthenticated
│   └── login/logout methods
│
├── designServiceProvider (Provider)
│   └── DesignService instance
│
└── myDesignsProvider (FutureProvider)
    ├── Fetches designer's designs
    ├── Auto-managed loading/error/data states
    └── Invalidate to refresh
```

## Backend Integration

```
API Endpoints Used:
├── POST /auth/login
│   └── Returns JWT token
│
├── GET /users/me
│   └── Returns user profile with role
│
├── GET /designs/me
│   ├── Requires: Bearer token + designer role
│   └── Returns: Array of design objects
│
└── POST /designs/
    ├── Requires: Bearer token + designer role
    ├── Body: {name, description, base_price, ...}
    └── Returns: Created design object
```

## Key Components

```
Models
├── Design (updated)
│   ├── name, base_price, base_image_url
│   └── Matches backend schema exactly
├── Fabric (new)
│   └── For future fabric selection
└── Color (new)
    └── For future color selection

Services
└── DesignService (extended)
    ├── getMyDesigns() → GET /designs/me
    └── createDesign() → POST /designs/

Providers
└── design_provider.dart (new)
    ├── myDesignsProvider (FutureProvider)
    └── designServiceProvider (Provider)

Screens
├── DesignerDashboardScreen (new)
│   ├── Lists designs
│   ├── Empty/Loading/Error/Data states
│   └── FAB to add designs
└── AddDesignScreen (new)
    ├── Form with validation
    └── Create new design

Widgets
└── DesignListItem (new)
    └── Reusable card for design display
```

This architecture follows Flutter best practices with clean separation of concerns, proper state management, and extensible design.
