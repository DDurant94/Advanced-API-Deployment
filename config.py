from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv('PASSWORD')

# connecting uri for mysql database
class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{PASSWORD}@localhost/advanced_e_commerce_db'
  CACHE_TYPE = 'SimpleCache'
  DEBUG = True