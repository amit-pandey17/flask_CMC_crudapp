# config.py
import logging
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Password123@localhost/crud_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'

    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
