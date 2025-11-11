#!/usr/bin/env python3
"""
Script to create test users for the Taarez application.
Run this script after the database is set up to create test users.

Usage:
    python create_test_users.py
"""

import sys
from sqlalchemy.orm import Session

from core.database import SessionLocal, engine
from core.security import hash_password
from models.user import User
from models.roles import UserRole

# Import Base to ensure models are registered
from core.database import Base


def create_test_users(db: Session):
    """Create test users for each role."""
    
    test_users = [
        {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Customer",
            "role": UserRole.CUSTOMER,
            "is_superuser": False,
        },
        {
            "email": "designer@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Designer",
            "role": UserRole.DESIGNER,
            "is_superuser": False,
        },
        {
            "email": "admin@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "Admin",
            "role": UserRole.ADMIN,
            "is_superuser": True,
        },
    ]
    
    created_count = 0
    skipped_count = 0
    
    for user_data in test_users:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        
        if existing_user:
            print(f"⏭️  User {user_data['email']} already exists, skipping...")
            skipped_count += 1
            continue
        
        # Validate password length (bcrypt limitation)
        password = user_data["password"]
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            print(f"❌ Password for {user_data['email']} is too long ({len(password_bytes)} bytes). Skipping...")
            continue
        
        # Create new user
        try:
            hashed_password = hash_password(password)
            new_user = User(
                email=user_data["email"],
                hashed_password=hashed_password,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                role=user_data["role"],
                is_superuser=user_data["is_superuser"],
                is_active=True,
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"✅ Created user: {user_data['email']} (Role: {user_data['role'].value})")
            created_count += 1
            
        except Exception as e:
            db.rollback()
            print(f"❌ Error creating user {user_data['email']}: {str(e)}")
    
    print(f"\n📊 Summary: {created_count} users created, {skipped_count} users skipped")
    return created_count


def main():
    """Main function to create test users."""
    print("🚀 Creating test users for Taarez application...")
    print("=" * 60)
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Create a database session
        db = SessionLocal()
        
        try:
            # Create test users
            created_count = create_test_users(db)
            
            if created_count > 0:
                print("\n✅ Test users created successfully!")
                print("\n📝 You can now log in with:")
                print("   - Customer: test@example.com / password123")
                print("   - Designer: designer@example.com / password123")
                print("   - Admin: admin@example.com / password123")
                return 0
            else:
                print("\n⚠️  No new users were created (they may already exist)")
                return 0
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
