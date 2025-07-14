from sqlalchemy import String, Integer, Column, ForeignKey, JSON, Boolean
from app.db.database import Base


class Trainers(Base):
    __tablename__ = 'trainers'
    id = Column(Integer, primary_key=True)
    user_profile = Column(Integer, ForeignKey('users.id'))
    experience = Column(Integer)
    aviable_times = Column(JSON)

    is_deleted = Column(Boolean, server_default='0')
