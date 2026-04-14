import os
import logging
from dotenv import load_dotenv

# try:
#     load_dotenv()
# except:
#     logging('error, .env file not found')
#     exit(0)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:dmscks0305dldia@localhost:5432/test_db') # 항상 같은 db라고 가정
    DB_USER = os.getenv('DB_USER', 'postgres') # 항상 서버는 하나의 admin/iam account가 확인한다고 가정
    DB_PASS = os.getenv('DB_PASS', 'dmscks0305dldia') # 비번이 걸려있을 경우에 .env파일에 넣을 것
    DB_NAME = os.getenv('DB_NAME', 'test_db') # 확인할 db이름. 지금으로선 그냥 저장하는거에 가까워서 비워둬도 상관x
    DB_PORT = os.getenv('DB_PORT', '5432') # 포트 번호. db가 어느 포트에 있는지.
    DB_HOST = os.getenv('DB_HOST', 'localhost') # db 호스트. 보통은 localhost일 예정.