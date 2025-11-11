#!/usr/bin/env python3
"""
Script to create test users in the database.
Run this after database migrations to set up initial test users.
"""

import sys
from sqlalchemy.orm import Session

from core.database import SessionLocal, engine
from core.security import hash_password
from models.user import User
from models.roles import UserRole


def create_test_users():
    """Create test users for development and testing."""
    db: Session = SessionLocal()

    try:
        # Test users to create
        test_users = [
            {
                "email": "test@example.com",
                "password": "password123",
                "first_name": "Test",
                "last_name": "User",
                "role": UserRole.CUSTOMER,
                "is_active": True,
                "is_superuser": False,
            },
            {
                "email": "designer@example.com",
                "password": "password123",
                "first_name": "Designer",
                "last_name": "User",
                "role": UserRole.DESIGNER,
                "is_active": True,
                "is_superuser": False,
            },
            {
                "email": "admin@example.com",
                "password": "password123",
                "first_name": "Admin",
                "last_name": "User",
                "role": UserRole.ADMIN,
                "is_active": True,
                "is_superuser": True,
            },
        ]

        created_count = 0
        skipped_count = 0

        for user_data in test_users:
            # Check if user already exists
            existing_user = (
                db.query(User).filter(User.email == user_data["email"]).first()
            )

            if existing_user:
                print(f"⏭️  User {user_data['email']} already exists, skipping...")
                skipped_count += 1
                continue

            # Create new user
            password = user_data.pop("password")
            hashed_password = hash_password(password)

            new_user = User(
                **user_data,
                hashed_password=hashed_password,
            )

            db.add(new_user)
            print(f"✅ Created user: {user_data['email']} ({user_data['role'].value})")
            created_count += 1

        db.commit()

        print(f"\n📊 Summary:")
        print(f"   Created: {created_count} users")
        print(f"   Skipped: {skipped_count} users (already existed)")
        print(f"\n🔐 Test Credentials:")
        print(f"   Customer: test@example.com / password123")
        print(f"   Designer: designer@example.com / password123")
        print(f"   Admin:    admin@example.com / password123")

        return True

    except Exception as e:
        print(f"❌ Error creating test users: {e}")
        db.rollback()
        return False

    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Creating test users...")
    print()

    success = create_test_users()

    if not success:
        sys.exit(1)

    print("\n✅ Test users setup complete!")
