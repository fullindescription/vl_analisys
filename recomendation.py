import numpy as np
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import UserPath


class Database:
    def __init__(self, db_connector: str) -> None:
        engine = create_engine(db_connector)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self) -> None:
        self.session.close()

    def get_all_data(self) -> tuple[list[UserPath], list[str], list[str]]:
        all_data = self.session.query(UserPath).limit(100).all()
        event_data = set(data.EventID for data in all_data)
        user_data = set(data.UserID for data in all_data)
        return all_data, list(event_data), list(user_data)


database = Database(db_connector="sqlite:///dump.db")
all_data, events, users = database.get_all_data()

matrix = np.zeros((len(events), len(users)), dtype=int)

for data in tqdm(all_data):
    event_index = events.index(data.EventID)
    user_index = users.index(data.UserID)
    matrix[event_index, user_index] = 1

print(matrix)

# TODO: Оптимизировать запросы в бд
