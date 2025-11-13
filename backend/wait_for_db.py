import time
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DB_URL = sys.argv[1] if len(sys.argv) > 1 else None
if not DB_URL:
    print("Usage: python wait_for_db.py <DATABASE_URL>")
    sys.exit(1)

max_attempts = 30
for attempt in range(max_attempts):
    try:
        engine = create_engine(DB_URL)
        conn = engine.connect()
        conn.close()
        print("Database is ready!")
        sys.exit(0)
    except OperationalError as e:
        print(f"Attempt {attempt+1}/{max_attempts}: DB not ready yet... {e}")
        time.sleep(2)
print("Database not ready after waiting.")
sys.exit(1)
