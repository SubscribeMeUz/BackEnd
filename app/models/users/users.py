from app.db.database import Base
from sqlalchemy import String, Integer, Column, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.web.schemas.users.roles import Roles


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)
    password = Column(String(255), unique=False)
    full_name = Column(String(255), unique=False)
    phone = Column(String(255), unique=True)
    
    role = Column(String(255), server_default=Roles.user)

    registred_date = Column(DateTime, default=func.now())

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    purchases = relationship("Purchases", back_populates="user")
    visitation_logs = relationship("VisitationLogs", back_populates="user")

    is_deleted = Column(Boolean, server_default='0')
