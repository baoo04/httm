from dao.admin_dao import AdminDAO
from utils.exceptions import UnAuthException
from werkzeug.security import check_password_hash

class AdminService:
    def __init__(self):
        self.admin_dao = AdminDAO()
        
    def login(self, username, password):
        admin = self.admin_dao.find_by_username(username)
        if not admin or not check_password_hash(admin.password, password):
            raise UnAuthException('Incorrect account or password')
        return admin
