from app.db.database import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, JSON, Time, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class AbonimentPackage(Base):
    __tablename__ = 'aboniment_packages'
    id = Column(Integer, primary_key=True)
    plan_name = Column(String(255))
    label = Column(String(255), nullable=True)
    title = Column(String(255))
    subtitle = Column(String(255))
    count = Column(Integer)
    expiry_days = Column(Integer)
    discount = Column(Integer)

    provider_id = Column(Integer, ForeignKey("providers.id"))
    provider = relationship("Providers", back_populates="aboniment_packages")
    aboniments = relationship("Aboniments", back_populates="aboniment_package")

    is_deleted = Column(Boolean, server_default='0')
