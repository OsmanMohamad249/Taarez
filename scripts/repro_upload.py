#!/usr/bin/env python3
import os, sys, time
sys.path.insert(0, 'backend')
# Ensure DB connection points to local ephemeral Postgres
os.environ.setdefault('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5433/postgres')
# Monkeypatch fastapi_limiter before importing the app
try:
    import fastapi_limiter
    try:
        from fastapi_limiter import depends as _depends
    except Exception:
        _depends = None
    class MockRateLimiter:
        def __init__(self, *args, **kwargs):
            pass
        async def __call__(self, request):
            return None
    if _depends is not None:
        _depends.RateLimiter = MockRateLimiter
    fastapi_limiter.FastAPILimiter.init = lambda *a, **k: None
except Exception:
    pass

from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=True)
base_headers = {"X-Forwarded-For": "127.0.0.1"}

email = f"smoke_debug_{int(time.time())}@example.com"
password = 'smokePass123'
print('Registering', email)
try:
    r = client.post('/api/v1/auth/register', json={'email':email,'password':password,'first_name':'D','last_name':'B'}, headers=base_headers)
    print('reg', r.status_code, r.text)
except Exception:
    import traceback; traceback.print_exc()
    sys.exit(1)

try:
    login = client.post('/api/v1/login/access-token', data={'username': email, 'password': password}, headers=base_headers)
    print('login', login.status_code, login.text)
    if login.status_code!=200:
        print('Login failed; aborting')
        sys.exit(1)
    token = login.json()['access_token']
except Exception:
    import traceback; traceback.print_exc()
    sys.exit(1)

headers={'Authorization': f'Bearer {token}'}
from io import BytesIO
files={'file': ('smoke.jpg', BytesIO(b'smoke-test-image-content'), 'image/jpeg')}
print('Calling upload-image...')
try:
    ru = client.post('/api/v1/measurements/upload-image', headers={**headers, **base_headers}, files=files)
    print('upload status', ru.status_code)
    print('upload body', ru.text)
except Exception:
    import traceback; traceback.print_exc()
    sys.exit(1)
