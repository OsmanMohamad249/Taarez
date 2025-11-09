```markdown
# Backend (FastAPI) - Tiraz

This folder contains the FastAPI backend application for Tiraz with secure configuration and modular structure.

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- PostgreSQL database (or use Docker Compose)

### Setup Steps

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and set required values (especially DATABASE_URL and SECRET_KEY)
   ```

   **IMPORTANT**: Generate a strong SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Run the application:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Docker (Local Development)

Using Docker Compose (recommended):
```bash
# From project root
docker-compose up backend
```

Building manually:
```bash
docker build -t tiraz-backend:dev -f Dockerfile .
docker run --rm -p 8000:8000 \
  -e DATABASE_URL=your_db_url \
  -e SECRET_KEY=your_secret_key \
  tiraz-backend:dev
```

## Configuration

All configuration is managed through environment variables using Pydantic BaseSettings with strict validation.

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:pass@host:port/db`)
- `SECRET_KEY`: Strong secret key for JWT signing (min 32 characters, no weak defaults allowed)

### Optional Environment Variables
- `ENVIRONMENT`: Application environment - `development`, `staging`, or `production` (default: development)
  - **Production mode automatically disables DEBUG**
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins (default: localhost only)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration (default: 30)
- `AI_SERVICE_URL`: URL for AI model service (default: http://ai-models:8000)
- `DEBUG`: Debug mode (default: true, automatically false in production)

### Environment-Specific Behavior

**Development Mode** (`ENVIRONMENT=development`):
- DEBUG enabled by default
- Relaxed CORS for local development
- Detailed error messages

**Staging Mode** (`ENVIRONMENT=staging`):
- Similar to development but can be configured for pre-production testing
- DEBUG can be explicitly controlled

**Production Mode** (`ENVIRONMENT=production`):
- DEBUG automatically disabled (cannot be overridden)
- Strict security validation enforced
- Minimal error exposure

See `.env.example` for complete configuration template with examples for each environment.

## API Endpoints

### Health Check
- `GET /health` - Basic health check

### Authentication (API v1)
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users (API v1)
- `GET /api/v1/users/me` - Get current user info (requires authentication)

### Measurements (API v1)
- `POST /api/v1/measurements` - Create measurement (requires authentication)
- `GET /api/v1/measurements` - List measurements (requires authentication)

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

For tests with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

**Note**: Database tests require a running PostgreSQL instance. Set up the database:
```bash
# Using Docker
docker run -d --name tiraz-test-db \
  -e POSTGRES_USER=tiraz \
  -e POSTGRES_PASSWORD=tiraz_password \
  -e POSTGRES_DB=tiraz_test_db \
  -p 5432:5432 \
  postgres:15

# Or use docker-compose
docker-compose up -d postgres
```

## Configuration Validation & Error Messages

The application provides clear, actionable error messages for configuration issues:

### Missing Required Fields
```
ValidationError: 2 validation errors for Settings
DATABASE_URL
  field required (type=value_error.missing)
SECRET_KEY
  field required (type=value_error.missing)
```

### Weak SECRET_KEY
```
ValidationError: SECRET_KEY appears to be a weak/default value. 
Please set a strong secret key in your environment variables.
```

### Invalid ENVIRONMENT
```
ValidationError: ENVIRONMENT must be one of ['development', 'staging', 'production'], got: invalid-env
```

### Short SECRET_KEY
```
ValidationError: ensure this value has at least 32 characters
```

All errors are caught at startup, preventing the application from running with invalid configuration.

## Security Features

✅ **Secure Configuration**
- Required environment variables with strict validation
- No hardcoded secrets in code
- Pydantic BaseSettings for type safety
- Environment-specific security controls
- Weak/default key detection and rejection

✅ **Authentication & Authorization**
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Secure token expiration

✅ **CORS Protection**
- Configurable allowed origins
- No wildcard origins by default
- Environment-specific CORS policies

✅ **Input Validation**
- Pydantic schemas for all endpoints
- Password length and complexity validation
- Email validation

## Project Structure

```
backend/
├── api/
│   └── v1/
│       ├── endpoints/    # API route handlers
│       │   ├── auth.py
│       │   ├── users.py
│       │   └── measurements.py
│       └── api.py        # API router aggregation
├── core/
│   ├── config.py         # Configuration (Pydantic BaseSettings)
│   ├── security.py       # Auth utilities (password hashing, JWT)
│   ├── database.py       # Database session management
│   └── deps.py           # FastAPI dependencies
├── models/               # SQLAlchemy models
│   ├── user.py
│   ├── roles.py
│   └── measurement.py
├── schemas/              # Pydantic schemas
│   ├── user.py
│   └── measurement.py
├── services/             # Business logic layer
├── tests/                # Test suite
│   ├── test_auth.py
│   ├── test_rbac.py
│   └── test_measurements.py
├── alembic/              # Database migrations
├── main.py               # FastAPI app initialization
└── requirements.txt
```

## Next Steps

- [ ] Add more comprehensive API tests
- [ ] Implement refresh tokens
- [ ] Add rate limiting
- [ ] Implement logging and monitoring
- [ ] Add API documentation with examples
```
