from app.db.database import Base
from sqlalchemy import String, Text, Integer, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Providers(Base):
    __tablename__ = 'providers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    about_description = Column(Text)
    location_latt = Column(String(255))
    location_long = Column(String(255))
    location_name = Column(String(255))
    necessary_tools = Column(String(255), server_default='')
    logo_path = Column(String(255))
    rules_description = Column(String(5000), server_default='')

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('Users', backref='providers')
    aboniments = relationship("Aboniments", back_populates="provider")
    aboniment_packages = relationship("AbonimentPackage", back_populates="provider")
    workout_times = relationship("WorkOutTimes", back_populates="provider")
    provider_tabs = relationship("ProviderTabs", back_populates="provider")
    photos = relationship("Photos", back_populates='provider')

    registred_date = Column(DateTime, default=func.now())

    is_deleted = Column(Boolean, server_default='0')
