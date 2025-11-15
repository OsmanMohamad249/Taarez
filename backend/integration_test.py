import httpx, json

base='http://127.0.0.1:8000'

# helper to print safe
def p(msg):
    print('---')
    print(msg)

# register a fresh user (ignore if duplicate)
try:
    reg = httpx.post(base+"/api/v1/auth/register", json={
        'email':'itest_user@example.com',
        'password':'itestpass123',
        'first_name':'IT', 'last_name':'User', 'role':'customer'
    }, timeout=10)
    p(f'register {reg.status_code} {reg.text}')
except Exception as e:
    p('register error: '+str(e))

# login to get token
try:
    login = httpx.post(base+"/api/v1/auth/login", data={'username':'itest_user@example.com','password':'itestpass123'}, timeout=10)
    p(f'login {login.status_code} {login.text}')
except Exception as e:
    p('login error: '+str(e))
    raise SystemExit(1)

if login.status_code==200:
    token=login.json().get('access_token')
    hdr={'Authorization':f'Bearer {token}'}
    files = [
        ('photo_front', ('front.png', open('/tmp/test_front.png','rb'), 'image/png')),
        ('photo_back', ('back.png', open('/tmp/test_back.png','rb'), 'image/png')),
        ('photo_left', ('left.png', open('/tmp/test_left.png','rb'), 'image/png')),
        ('photo_right', ('right.png', open('/tmp/test_right.png','rb'), 'image/png')),
    ]
    data={'height':'170','weight':'70'}
    try:
        resp = httpx.post(base+"/api/v1/measurements/process", headers=hdr, files=files, data=data, timeout=30)
        p(f'process {resp.status_code}')
        try:
            p(json.dumps(resp.json(), indent=2))
        except Exception:
            p(resp.text)
    except Exception as e:
        p('process error: '+str(e))
else:
    p('could not login')
