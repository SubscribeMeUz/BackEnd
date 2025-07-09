from app.db.database import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Purchases(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, index=True)

    aboniment_id = Column(Integer, ForeignKey('aboniments.id'))
    aboniment = relationship("Aboniments", back_populates='purchases', foreign_keys=[aboniment_id])

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", backref='purchases', foreign_keys=[user_id])

    used_count = Column(Integer, server_default='0')
    status = Column(String(255), server_default="new")

    recorded_date = Column(DateTime, server_default=func.now())

    visitation_logs = relationship("VisitationLogs", back_populates="purchase")

    is_deleted = Column(Boolean, server_default='0')
