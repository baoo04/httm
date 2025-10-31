from dao.dao import get_db_connection
from models.traffic_sign_dataset import TrafficSignDataset
from dao.sample_dao import SampleDAO

class DatasetDAO:
    def find_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignDataset")
        dataset_rows = cursor.fetchall()

        datasets = []
        sample_dao = SampleDAO()

        for dataset_row in dataset_rows:
            dataset = TrafficSignDataset(**dataset_row)
            images = sample_dao.find_all_by_dataset_id(dataset.id)

            image_dicts = []
            for img in images:
                img_dict = {k: v for k, v in img.__dict__.items() if not k.startswith('_')}
                image_dicts.append(img_dict)

            dataset_dict = {k: v for k, v in dataset.__dict__.items() if not k.startswith('_')}
            dataset_dict['images'] = image_dicts

            datasets.append(dataset_dict)

        cursor.close()
        conn.close()
        return datasets
    
    def find_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignDataset WHERE id=%s LIMIT 1", (id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return TrafficSignDataset(**row)
        return None
