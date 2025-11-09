"""
User role definitions.
"""

import enum


class UserRole(str, enum.Enum):
    """Enum for user roles in the system."""

    ADMIN = "admin"
    CUSTOMER = "customer"
    DESIGNER = "designer"
    TAILOR = "tailor"
