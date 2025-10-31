from dao.dataset_dao import DatasetDAO

class DatasetService:
    def __init__(self):
        self.dataset_dao = DatasetDAO()

    def get_all_datasets(self):
        datasets = self.dataset_dao.find_all()
        return datasets