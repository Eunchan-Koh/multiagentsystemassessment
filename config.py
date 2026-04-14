import os
import logging
from dotenv import load_dotenv

# try:
#     load_dotenv()
# except:
#     logging('error, .env file not found')
#     exit(0)

# moidify the values if needed.
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:dmscks0305dldia@localhost:5432/test_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'dmscks0305dldia')
    DB_NAME = os.getenv('DB_NAME', 'test_db')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_HOST = os.getenv('DB_HOST', 'localhost') 