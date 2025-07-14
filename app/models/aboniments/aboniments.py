from app.db.database import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Aboniments(Base):
    __tablename__ = 'aboniments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    label = ''
    title = ''
    subtitle = ''

    price = Column(Integer)
    available_days = Column(JSON)
    working_hours = Column(JSON)

    provider_id = Column(Integer, ForeignKey('providers.id'))
    workout_time_id = Column(Integer, ForeignKey('workout_times.id'))
    provider_tab_id = Column(Integer, ForeignKey('provider_tabs.id'))
    aboniment_package_id = Column(Integer, ForeignKey('aboniment_packages.id'))
    provider = relationship('Providers', back_populates='aboniments')
    workout_time = relationship('WorkOutTimes', back_populates='aboniments')
    provider_tab = relationship("ProviderTabs", back_populates='aboniments')
    aboniment_package = relationship("AbonimentPackage", back_populates='aboniments')
    purchases = relationship('Purchases', back_populates='aboniment')
    purchasing_requests = relationship("PurchasingRequests", back_populates='aboniment')

    is_deleted = Column(Boolean, server_default='0')
