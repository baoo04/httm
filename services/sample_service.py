from dao.sample_dao import SampleDAO
from utils.exceptions import NotFoundException

class SampleService:
    def __init__(self):
        self.sample_dao = SampleDAO()

    def get_sample_by_id(self, id):
        sample = self.sample_dao.find_by_id(id)
        if not sample:
            raise NotFoundException(f'Sample not found')
        return sample

