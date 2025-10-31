from dao.dao import get_db_connection
from models.admin import Admin

class AdminDAO:
    def find_by_username(self, username):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tblAdmin WHERE username=%s LIMIT 1", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Admin(**row)
        return None
