"""
Database models for Tiraz application
"""
from datetime import datetime
from app import db


class Item(db.Model):
    """Item model representing a styled item in the Tiraz application"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    style = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Item {self.name}>'
    
    def to_dict(self):
        """Convert item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'style': self.style,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
