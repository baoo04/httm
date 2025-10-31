from dao.dao import get_db_connection
from models.traffic_sign_sample import TrafficSignSample

class SampleDAO:
    def find_all_by_dataset_id(self, dataset_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignSample where dataset_id=%s and is_trained=0", (dataset_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        models = [TrafficSignSample(**row) for row in result]
        return models
    
    def find_all_by_ids(self, ids):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        format_strings = ','.join(['%s'] * len(ids))
        cursor.execute(f"SELECT * FROM tblTrafficSignSample WHERE id IN ({format_strings}) and is_trained=0", tuple(ids))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        samples = [TrafficSignSample(**row) for row in result]
        return samples
    
    def find_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignSample WHERE id=%s LIMIT 1", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return TrafficSignSample(**row)
        return None
    
    def mark_as_trained(self, ids):
        conn = get_db_connection()
        cursor = conn.cursor()
        format_strings = ','.join(['%s'] * len(ids))
        cursor.execute(f"UPDATE tblTrafficSignSample SET is_trained = 1 WHERE id IN ({format_strings})", tuple(ids))
        conn.commit()
        cursor.close()
        conn.close()
