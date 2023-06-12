import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv


load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')

engine = create_engine(
    f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}', 
    echo=True)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
