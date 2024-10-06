from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from database import db
from schema import ma
from limiter import limiter
from caching import cache
from sqlalchemy.orm import Session

from models.customer import Customer
from models.customerAccount import CustomerAccount
from models.order import Order
from models.product import Product
from models.orderProduct import OrderProducts
from models.role import Role
from models.customerManagementRole import CustomerManagementRole

from routes.customerBP import customer_blueprint
from routes.customerAccountBP import customer_account_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.roleBP import role_blueprint

# swagger url http://127.0.0.1:5000/api/docs
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

#adding the app name
swagger_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={
    'app_name': "E-Commerce API"
  }
)

# creating the app
def create_app(config_name):
  app = Flask(__name__)
  
  try:
    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app)
  except Exception as e:
    print(f"Error creating app: {e}")
    raise e
  
  return app
  

# endpoints config for the app to be usable (base of all endpoints)
def blue_print_config(app):
  app.register_blueprint(customer_blueprint, url_prefix='/customers')
  app.register_blueprint(customer_account_blueprint,url_prefix='/customer-accounts')
  app.register_blueprint(order_blueprint,url_prefix='/orders')
  app.register_blueprint(product_blueprint,url_prefix='/products')
  app.register_blueprint(role_blueprint,url_prefix='/roles')
  app.register_blueprint(swagger_blueprint,url_prefix=SWAGGER_URL)
  
# setting endpoint limits
def configure_rate_limit():
  limiter.limit("100 per day")(customer_blueprint)
  limiter.limit("100 per day")(customer_account_blueprint)
  limiter.limit("100 per day")(order_blueprint)
  limiter.limit("100 per day")(product_blueprint)
  limiter.limit("100 per day")(role_blueprint)
  limiter.limit("100 per day")(swagger_blueprint)

if __name__ == '__main__':
  app = create_app('DevelopmentConfig')
  
  blue_print_config(app)
  configure_rate_limit()
  
  with app.app_context():
    db.create_all()
    
  app.run(debug=True)