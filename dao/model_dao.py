from dao.dao import get_db_connection
from models.traffic_sign_model import TrafficSignModel

class ModelDAO:
    def get_models(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignModel")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        models = [TrafficSignModel(**row) for row in result]
        return models

    def save_model(self, model: TrafficSignModel):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO tblTrafficSignModel 
                (name, version, pre, recall, f1_score, is_active, sample_quantity, dataset_id, path)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (model.name, model.version, model.pre, model.recall, model.f1_score,
                             model.is_active, model.sample_quantity, model.dataset_id, model.path))
        conn.commit()
        cursor.close()
        conn.close()
