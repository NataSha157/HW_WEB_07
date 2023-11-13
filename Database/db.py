import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URI: postgresql://username:password@domain:port/database_name
file_config = pathlib.Path(__file__).parent.joinpath('config.ini') #./config.ini
config = configparser.ConfigParser()
config.read(file_config)

# username = config.get('DEV_DB', 'USER')
# password = config.get('DEV_DB', 'PASSWORD')
# domain = config.get('DEV_DB', 'DOMAIN')
# port = config.get('DEV_DB', 'PORT')
# database_name = config.get('DEV_DB', 'DB_NAME')

username = 'postgres'
password = '9876598765'
domain = 'localhost'
port = '5432'
database_name = 'hw_web_07'

URI = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'


engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)
session = DBSession()



