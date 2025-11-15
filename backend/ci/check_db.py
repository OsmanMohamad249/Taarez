import os
from sqlalchemy import create_engine, text
from core.config import settings


def main():
    test_email = os.environ.get('TEST_EMAIL') or 'ci_smoke@example.com'
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        # find test user
        res = conn.execute(text("SELECT id FROM users WHERE email=:email LIMIT 1"), {'email': test_email})
        user_id = res.scalar()
        if not user_id:
            print(f'ERROR: test user not found in DB for email={test_email}')
            raise SystemExit(2)
        # find most recent measurement for that user
        res2 = conn.execute(text("SELECT id, confidence_score FROM measurements WHERE user_id=:uid ORDER BY processed_at DESC LIMIT 1"), {'uid': user_id})
        row = res2.fetchone()
        if not row:
            print('ERROR: no measurement found for user', user_id)
            raise SystemExit(3)
        print('OK: found measurement', row[0], 'confidence=', row[1])


if __name__ == '__main__':
    main()
