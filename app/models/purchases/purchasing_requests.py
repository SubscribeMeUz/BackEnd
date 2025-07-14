from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base


class PurchasingRequests(Base):
    __tablename__ = 'purchasing_requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    aboniment_id = Column(Integer, ForeignKey('aboniments.id'))
    purchase_id = Column(Integer, ForeignKey('purchases.id'), nullable=True, server_default=None)

    aboniment = relationship("Aboniments", back_populates='purchasing_requests')
    user = relationship("Users", backref='purchasing_requests')
    status = Column(String(255), server_default='new')
    recorded_date = Column(DateTime, default=func.now())

    is_deleted = Column(Boolean, server_default='0')
