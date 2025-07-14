from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Photos(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    path = Column(String(255))
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=True)

    provider = relationship("Providers", back_populates='photos')
