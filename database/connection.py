import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
db_echo = os.getenv("DB_ECHO").lower() in ["true", "yes", "1"]

db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(db_url, echo=db_echo)

Session = sessionmaker(bind=engine)