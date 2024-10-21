import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import UserPath, EventToCategory


class RecommendationSystem:
    def __init__(self, db_connector: str) -> None:
        engine = create_engine(db_connector)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self) -> None:
        self.session.close()

    def get_all_data(self) -> list[UserPath]:
        # user_data = self.session.query(UserPath).distinct().all()
        user_data = self.session.query(UserPath).distinct().limit(100000).all()
        return user_data

    def get_all_events_id(self) -> list[str]:
        event_data = self.session.query(EventToCategory).all()

        return [data.EventID for data in event_data]


recommend_system = RecommendationSystem(db_connector="sqlite:///dump.db")
events = recommend_system.get_all_events_id()
table = {}
for event in events:
    table[event] = []

all_data = recommend_system.get_all_data()
for data in all_data:
    table[data.EventID].append(data.UserID)
