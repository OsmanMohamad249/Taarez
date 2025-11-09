# Tiraz Admin Portal (Next.js)

## Overview
This is the Next.js admin portal for Tiraz - an AI tailoring platform. The admin portal is designed for administrators and management to oversee and manage the platform.

## Project Structure
```
admin-portal/
├── app/                    # Next.js 14 App Router
│   ├── (auth)/            # Authentication routes
│   │   └── login/         # Login page
│   ├── admin/             # Admin dashboard
│   │   └── page.tsx       # Dashboard home
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Root page (redirects to login)
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── forms/            # Form components
│   └── layout/           # Layout components
├── lib/                  # Core libraries
│   ├── api/              # API service functions
│   │   ├── config.ts     # Axios configuration
│   │   ├── auth.ts       # Authentication API
│   │   ├── designs.ts    # Design management API
│   │   ├── users.ts      # User management API
│   │   └── categories.ts # Category management API
│   ├── types/            # TypeScript interfaces
│   │   └── index.ts      # Shared type definitions
│   └── utils/            # Helper functions
│       ├── cn.ts         # Class name utility
│       └── format.ts     # Formatting utilities
├── store/                # State management (Zustand)
│   └── auth-store.ts     # Authentication state
├── public/               # Static assets
├── .env.example          # Environment variables template
├── .env.local            # Local environment variables (not committed)
├── next.config.js        # Next.js configuration
├── tailwind.config.ts    # Tailwind CSS configuration
└── tsconfig.json         # TypeScript configuration
```

## Tech Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3
- **State Management**: Zustand 4
- **HTTP Client**: Axios 1.6
- **Icons**: Lucide React

## Features
✅ Admin authentication with JWT
✅ Role-based access control (admin only)
✅ Admin dashboard
✅ API service layer with Axios interceptors
✅ TypeScript type definitions
✅ Zustand state management
✅ Responsive UI with Tailwind CSS
✅ Auto token refresh handling

## Setup Instructions

### Prerequisites
- Node.js (v20 or higher)
- npm or yarn
- Backend API running on http://localhost:8000

### Installation
1. Navigate to the admin portal directory:
```bash
cd admin-portal
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
cp .env.example .env.local
```

4. Update environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Development
Run the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production
```bash
npm run build
npm start
```

## API Configuration
The admin portal connects to the FastAPI backend through the API service layer:
- Base URL: Configured in `.env.local`
- API Version: `/api/v1`
- Authentication: JWT Bearer token
- Auto token injection via Axios interceptors

## Authentication Flow
1. User visits root URL → Redirected to `/login`
2. User enters admin credentials
3. API validates credentials and returns JWT token
4. Token stored in localStorage
5. Token automatically attached to all API requests
6. On 401 response, user redirected to login

## Access Control
- **Only admin users** can access the admin portal
- Non-admin users are rejected during login
- Token validation on protected routes
- Automatic logout on unauthorized access

## State Management
Using Zustand for lightweight state management:
- **Auth Store**: User authentication state
- Persisted authentication status
- Token management
- User profile data

## API Services
All API interactions are centralized in `lib/api/`:
- **auth.ts**: Login, register, logout
- **designs.ts**: Design CRUD operations
- **users.ts**: User management
- **categories.ts**: Category operations

## Styling
Built with Tailwind CSS for:
- Responsive design
- Consistent styling
- Utility-first approach
- Dark mode support (future)

## Next Steps
- [ ] Implement user management dashboard
- [ ] Add design management interface
- [ ] Create category management
- [ ] Add data visualization charts
- [ ] Implement real-time notifications
- [ ] Add export/import functionality
- [ ] Create admin user roles and permissions
- [ ] Add audit logs and activity tracking

## Development Guidelines

### Adding New Pages
1. Create page in `app/` directory
2. Use TypeScript for type safety
3. Follow existing patterns for API calls
4. Use Zustand store for state management

### Adding New API Endpoints
1. Define types in `lib/types/index.ts`
2. Create API function in appropriate `lib/api/*.ts` file
3. Use `apiClient` from `lib/api/config.ts`
4. Handle errors consistently

### Styling Components
```tsx
import { cn } from '@/lib/utils/cn';

<div className={cn(
  'base-classes',
  condition && 'conditional-classes'
)}>
```

## Testing
```bash
# Run linter
npm run lint

# Build check
npm run build
```

## Troubleshooting
- **API connection errors**: Verify backend is running on port 8000
- **Authentication failures**: Check JWT token in localStorage
- **CORS errors**: Configure CORS settings in FastAPI backend
- **Build errors**: Clear `.next` cache and rebuild

## Security Notes
- JWT tokens stored in localStorage (consider httpOnly cookies for production)
- Always use HTTPS in production
- Implement CSRF protection for sensitive operations
- Add rate limiting for API endpoints
- Regular security audits and dependency updates

## License
MIT License
