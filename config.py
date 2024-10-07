from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# connecting uri for postgras database
class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = 'postgresql://e_commerce_api_r2mn_user:pddIAMcxJxjyDeYsH5YV3b9q5nDfxaUP@dpg-cs1f00dds78s73b630sg-a.oregon-postgres.render.com/e_commerce_api_r2mn'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = 'SimpleCache'
  
  