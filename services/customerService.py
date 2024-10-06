from sqlalchemy.orm import Session
from database import db
from circuitbreaker import circuit
from sqlalchemy import select

from models.customer import Customer
from models.customerAccount import CustomerAccount
from models.order import Order
from models.orderProduct import OrderProducts

def fallback_function(customer):
  return None

# adding customer and circuit breaker if name == "Failure keeping the integrity of information if the API is having problems"
@circuit(failure_threshold=1,recovery_timeout=10,fallback_function=fallback_function)
def save(customer_data):
  try:
    if customer_data['name'] == "Failure":
      raise Exception("Failure condition triggered")
    
    with Session(db.engine) as session:
      with session.begin():
        new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
        session.add(new_customer)
        session.commit()  
      session.refresh(new_customer)
      return new_customer
    
  except Exception as e:
    raise e

# getting all customers
def find_all():
  query = select(Customer)
  customers = db.session.execute(query).scalars().all()
  return customers

def find_all_pagination(page=1,per_page=10):
  customers = db.paginate(select(Customer), page=page, per_page=per_page)
  return customers

# getting customer by ID
def find_by_id(id):
  query = select(Customer).filter_by(id=id)
  customer = db.session.execute(query).unique().scalar_one_or_none()
  return customer

# updating customer information
def update(customer_data, id):
  with Session(db.engine) as session:
    with session.begin():
      customer = db.session.execute(db.select(Customer).where(Customer.id == id)).unique().scalar_one_or_none()
      customer.id = customer_data['id']
      customer.name = customer_data['name']
      customer.email = customer_data['email']
      customer.phone = customer_data['phone']
    db.session.commit()
  return customer

# deleting customer and all associations with customer (customer account, and orders)
def delete(id):
  with Session(db.engine) as session:
    with session.begin():
      customer = session.execute(db.select(Customer).where(Customer.id == id)).unique().scalar_one_or_none()
      customer_account = session.execute(db.select(CustomerAccount).where(CustomerAccount.customer_id == id)).unique().scalar_one_or_none()
      customer_orders = session.execute(db.select(Order).where(Order.customer_id == id)).scalars().all()
      order_items = session.execute(db.select(OrderProducts).where(OrderProducts.order_id.in_([order.id for order in customer_orders]))).scalars().all()

      for item in order_items:
          session.delete(item)

      for order in customer_orders:
          session.delete(order)

      if customer_account is not None:
          session.delete(customer_account)

      if customer is not None:
          session.delete(customer)
      else:
          return None
          
    session.commit()
  return "successful"