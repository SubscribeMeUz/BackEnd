from app.db.database import Base
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ProviderTabs(Base):
    __tablename__ = 'provider_tabs'
    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    value = Column(String(255))
    title = Column(String(255))

    provider_id = Column(Integer, ForeignKey("providers.id"))
    provider = relationship("Providers", back_populates='provider_tabs')
    aboniments = relationship("Aboniments", back_populates='provider_tab')

    is_deleted = Column(Boolean, server_default='0')
