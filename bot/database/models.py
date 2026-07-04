from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MessageHistory(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
