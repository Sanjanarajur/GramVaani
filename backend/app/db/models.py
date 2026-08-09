from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .connection import Base


#User Role
class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    
#User Table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(name={self.name}, role={self.role})"
    

class Grievance(Base):
    __tablename__ = "grievances"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    category = Column(String(100))
    priority = Column(String(50))
    region = Column(String(150))
    latitude = Column(String(50))
    longitude = Column(String(50))
    solution = Column(Text)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="grievances")
    