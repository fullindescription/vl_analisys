import numpy as np
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import UserPath


class Database:
    def __init__(self, db_connector: str) -> None:
        engine = create_engine(db_connector)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self) -> None:
        self.session.close()

    def get_all_data(self) -> tuple[list[UserPath], list[str], list[str]]:
        all_data = (
            self.session.query(UserPath)
            .filter(UserPath.Act != "EventShow")
            # .limit(10000)
            .all()
        )
        event_data = set(data.EventID for data in all_data)
        user_data = set(data.UserID for data in all_data)
        return all_data, list(event_data), list(user_data)


class RecomendSystem:
    def __init__(
        self, data: tuple[list[UserPath]], features: list[str], users: list[str]
    ) -> None:
        self.users = users
        self.features = features
        features_count = len(features)
        users_count = len(users)
        print(f"Размеры матрицы: {features_count}x{users_count}")

        matrix = np.zeros((features_count, users_count), dtype=int)

        for data in tqdm(all_data):
            event_index = features.index(data.EventID)
            user_index = users.index(data.UserID)
            if data.Act == "SuccessPurchase":
                matrix[event_index, user_index] = 3
            elif data.Act == "BuyWithContact":
                matrix[event_index, user_index] = 2
            elif data.Act == "EventPreBuy":
                matrix[event_index, user_index] = 1

        start_time = datetime.now()
        U, lmbd, V = np.linalg.svd(matrix)
        k = features_count

        S_k = np.zeros((U.shape[1], V.shape[0]))
        S_k[:k, :k] = np.diag(lmbd[:k])

        self.predicted_matrix = U[:, :k] @ S_k[:k, :k] @ V[:k, :]
        end_time = datetime.now()

        print(end_time - start_time)

    def predict(self, user_id: str) -> list[str]:
        user_index = self.users.index(user_id)
        user_predict = self.predicted_matrix[:, user_index]

        top_indices = np.argsort(user_predict)[-3:][::-1]

        return [self.features[i] for i in top_indices]


if __name__ == "__main__":
    database = Database(db_connector="sqlite:///dump.db")
    all_data, features, users = database.get_all_data()
    rec_system = RecomendSystem(all_data, features, users)
    recomendations = rec_system.predict("9b933ab3010b5e8870cb7ebb36d8d9ae")
    print(recomendations)
