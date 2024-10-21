from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class MainPage(Base):
    __tablename__ = "MainPage"

    Time = Column(DateTime, primary_key=True)
    UserID = Column(Integer, nullable=False)
    SessionID = Column(Integer, nullable=False)
    DeviceType = Column(String, nullable=False)
    Act = Column(String, nullable=False)
    Block = Column(String, nullable=False)
    Extra = Column(String)


class UserPath(Base):
    __tablename__ = "UserPath"

    UserID = Column(Integer, primary_key=True)
    DeviceType = Column(String, nullable=False)
    Act = Column(String, nullable=False)
    EventID = Column(Integer, nullable=False)


class EventToCategory(Base):
    __tablename__ = "Event_to_Category"

    EventID = Column(String, primary_key=True)
    Type = Column(String, nullable=False)
    AgeRestriction = Column(String, nullable=True)
    Categories = Column(String, nullable=False)
