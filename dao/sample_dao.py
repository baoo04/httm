from dao.dao import get_db_connection
from models.traffic_sign_sample import TrafficSignSample

class SampleDAO:
    def get_images(self, dataset_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignSample where dataset_id=%s", (dataset_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        models = [TrafficSignSample(**row) for row in result]
        return models
    