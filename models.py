from sqlalchemy import Column, String, Integer
from database import Base

class URL(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True)
    short_path = Column(String, unique=True, index=True)
