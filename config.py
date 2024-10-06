from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
  
  