from app.db.database import Base
from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, JSON, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class WorkOutTimes(Base):
    __tablename__ = 'workout_times'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    from_time = Column(Time)
    to_time = Column(Time)
    discount = Column(Integer)

    provider_id = Column(Integer, ForeignKey("providers.id"))
    provider = relationship("Providers", back_populates="workout_times")
    aboniments = relationship("Aboniments", back_populates="workout_time")

    is_deleted = Column(Boolean, server_default='0')
