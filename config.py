from dotenv import load_dotenv
import os

load_dotenv(override=True)
DATABASE_URL = os.getenv('DATABASE_URL')

# connecting uri for postgras database
class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = DATABASE_URL
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = 'SimpleCache'
  
  