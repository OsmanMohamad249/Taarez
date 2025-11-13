import io
from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=True)

# helper
import time
email = f"dbg_{int(time.time())}@example.com"
password = "testpass123"

# register
r = client.post('/api/v1/auth/register', json={'email':email,'password':password,'first_name':'D','last_name':'B'})
print('register', r.status_code, r.text)
# login
r = client.post('/api/v1/auth/login', data={'username':email,'password':password})
print('login', r.status_code, r.text)
token = r.json().get('access_token')

files = {
    "photo_front": ("front.jpg", io.BytesIO(b"fake image content"), "image/jpeg"),
    "photo_back": ("back.jpg", io.BytesIO(b"fake image content"), "image/jpeg"),
    "photo_left": ("left.jpg", io.BytesIO(b"fake image content"), "image/jpeg"),
    "photo_right": ("right.jpg", io.BytesIO(b"fake image content"), "image/jpeg"),
}

r = client.post('/api/v1/measurements/upload', files=files, headers={'Authorization':f'Bearer {token}'})
print('upload', r.status_code)
print(r.text)
