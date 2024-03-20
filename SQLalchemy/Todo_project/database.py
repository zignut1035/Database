from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo = False, future = True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    userName = Column(String, unique=True)
    passWord = Column(String)
    items = relationship("Item", back_populates="user")

class Item(Base):
    __tablename__ = "items"
    itemId = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)  
    added_time = Column(DateTime, default=datetime.now)  
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="items")

Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)