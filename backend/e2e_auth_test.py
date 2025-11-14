import os
import sys
import json
from uuid import UUID

from fastapi.testclient import TestClient

# Ensure settings read env vars
# DATABASE_URL and SECRET_KEY must be set in environment
from main import app

from core.database import SessionLocal
from models.user import User

client = TestClient(app)


def pretty(resp):
    try:
        return json.dumps(resp.json(), indent=2)
    except Exception:
        return resp.text


def register_with_role(email, password, role, first="Test", last="User"):
    payload = {
        "email": email,
        "password": password,
        "first_name": first,
        "last_name": last,
        "role": role,
    }
    r = client.post("/api/v1/auth/register", json=payload)
    print(f"REGISTER {role.upper()} {email} -> status {r.status_code}")
    print(pretty(r))
    return r


def login(email, password):
    data = {"username": email, "password": password}
    r = client.post("/api/v1/auth/login", data=data)
    print(f"LOGIN {email} -> status {r.status_code}")
    print(pretty(r))
    return r


def get_user_from_db(email):
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.email == email).first()
        return u
    finally:
        db.close()


if __name__ == "__main__":
    # Read env or exit
    db_url = os.getenv("DATABASE_URL")
    sk = os.getenv("SECRET_KEY")
    if not db_url or not sk:
        print("ERROR: DATABASE_URL and SECRET_KEY must be set in environment")
        sys.exit(2)

    print("Starting end-to-end auth tests\n")

    # Test user details
    customer_email = "customer@example.com"
    designer_email = "designer@example.com"
    admin_email = "admin@example.com"
    pw = "securepass123"

    # 1. Register Customer
    r1 = register_with_role(customer_email, pw, "customer")

    # 2. Login Customer
    r2 = login(customer_email, pw)

    # 3. Attempt to register Designer
    r3 = register_with_role(designer_email, pw, "designer")

    # 4. Attempt to login Designer
    r4 = login(designer_email, pw)

    # 5. Attempt to register Admin
    r5 = register_with_role(admin_email, pw, "admin")

    # 6. Confirm password hashing works for Customer
    user = get_user_from_db(customer_email)
    if user:
        print(f"\nDB user present: email={user.email}, hashed_password={user.hashed_password}")
        if user.hashed_password == pw:
            print("PASSWORD stored in DB is plaintext -> FAILURE")
        else:
            print("PASSWORD stored in DB is hashed (not equal to plaintext) -> OK")
    else:
        print("Customer user not found in DB")

    # Check tokens from login
    if r2.status_code == 200:
        token = r2.json().get("access_token")
        print(f"Customer token: {token[:20]}... (len={len(token)})")
    else:
        print("Customer login failed, no token")

    if r4.status_code == 200:
        token2 = r4.json().get("access_token")
        print(f"Designer token: {token2[:20]}... (len={len(token2)})")
    else:
        print("Designer login failed, no token")

    print('\nDone')
