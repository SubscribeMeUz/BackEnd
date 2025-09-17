import typing
from app.db.database import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class TgSettings(Base):
    __tablename__ = 'tgsettings'
    id = Column(Integer, primary_key= True)
    chanel_name = Column(String)
    is_active = Column(Boolean, default=True) 

    provider_id = Column(Integer, ForeignKey('providers.id'))
    provider = relationship("Providers", back_populates='tgsettings', foreign_keys=[provider_id])