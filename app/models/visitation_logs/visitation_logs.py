from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class VisitationLogs(Base):
    __tablename__ = 'visitation_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    purchase_id = Column(Integer, ForeignKey('purchases.id'))

    user = relationship("Users", back_populates="visitation_logs")
    purchase = relationship("Purchases", back_populates="visitation_logs")
    recorded_date = Column(DateTime, server_default=func.now())

    is_deleted = Column(Boolean, server_default='0')
