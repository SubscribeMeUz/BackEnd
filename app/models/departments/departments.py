from app.db.database import Base
from sqlalchemy import Column, String, Integer, Boolean


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    is_deleted = Column(Boolean, server_default='0')
