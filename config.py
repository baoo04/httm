# F:\HTTM\config.py

import os

class Config:
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'baodang123'
    DB_NAME = 'httm_db'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
