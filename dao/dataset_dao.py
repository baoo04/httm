from dao.dao import get_db_connection
from models.traffic_sign_dataset import TrafficSignDataset
from dao.sample_dao import SampleDAO

class DatasetDAO:
    def get_datasets(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblTrafficSignDataset")
        dataset_rows = cursor.fetchall()

        datasets = []
        sample_dao = SampleDAO()

        for dataset_row in dataset_rows:
            dataset = TrafficSignDataset(**dataset_row)
            images = sample_dao.get_images(dataset.id)

            # Chuyển ảnh sang dict nhưng loại bỏ các key không serializable
            image_dicts = []
            for img in images:
                img_dict = {k: v for k, v in img.__dict__.items() if not k.startswith('_')}
                image_dicts.append(img_dict)

            # Dataset cũng chuyển tương tự
            dataset_dict = {k: v for k, v in dataset.__dict__.items() if not k.startswith('_')}
            dataset_dict['images'] = image_dicts

            datasets.append(dataset_dict)

        cursor.close()
        conn.close()
        return datasets
