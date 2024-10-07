from sqlalchemy.orm import Session
from database import db
from sqlalchemy import select
from werkzeug.security import generate_password_hash,check_password_hash

from utils.util import encode_token

from models.customer import Customer
from models.customerAccount import CustomerAccount
from models.role import Role
from models.customerManagementRole import CustomerManagementRole as CMR

# adding account with an associated role attached to the account
def save(customer_account_data):
  with Session(db.engine) as session:
    with session.begin():
      try: 
        user = session.execute(db.select(CustomerAccount).where(CustomerAccount.username == customer_account_data['username'])).scalar_one_or_none()
        if user:
          raise ValueError("Customer Account already exists")
        
        savepoint = session.begin_nested()
        
        new_customer_account = CustomerAccount(username=customer_account_data['username'],password=generate_password_hash(customer_account_data['password']),customer_id=customer_account_data['customer_id'],role=customer_account_data['role'])
        session.add(new_customer_account)
        session.flush()
        
        role = session.execute(db.select(Role).where(Role.role_name == new_customer_account.role)).scalar_one_or_none()
        
        if role is not None:
          adding_customer_to_role = CMR(customer_management_id=new_customer_account.id,role_id=role.id)
          session.add(adding_customer_to_role)
        else:
          raise ValueError("Role not found")
          
      except Exception:
        savepoint.rollback()
        return None
      
      session.commit()
    session.refresh(new_customer_account)
  return new_customer_account
  
# getting all accounts
def find_all():
  query = select(CustomerAccount).join(Customer).where(Customer.id == CustomerAccount.customer_id)
  customer_accounts = db.session.execute(query).unique().scalars().all()
  return customer_accounts

def login_customer(username,password):
  user = (db.session.execute(db.select(CustomerAccount).where(CustomerAccount.username == username)).unique().scalar_one_or_none())
  if user:
    if check_password_hash(user.password,password):
      role_names = [role.role_name for role in user.roles]
      auth_token = encode_token(user.id,role_names)
      print(auth_token)
      resp = {
        "status": "success",
        "message": "Successfully logged in",
        'auth_token': auth_token
      }
      return resp
    else:
      return None
  else:
    return None

# getting account by ID 
def find_by_id(id):
  query = select(CustomerAccount).join(Customer).where(Customer.id == CustomerAccount.customer_id).filter_by(id=id)
  account = db.session.execute(query).unique().scalar_one_or_none()
  return account

# updating account information
def update(customer_update_data, id):
  with Session(db.engine) as session:
    with session.begin():
      account = db.session.execute(db.select(CustomerAccount).where(CustomerAccount.id == id)).unique().scalar_one_or_none()
      account.id = customer_update_data['id']
      account.username = customer_update_data['username']
      account.password = generate_password_hash(customer_update_data['password'])
      account.role = customer_update_data['role']
    db.session.commit()
  return account
      
# deleting account 
def delete(id):
  with Session(db.engine) as session:
    with session.begin():
      customer_account = db.session.execute(db.select(CustomerAccount).where(CustomerAccount.id == id)).unique().scalar_one_or_none()
      if customer_account is not None:
        db.session.delete(customer_account)
      else:
        return None
    db.session.commit()
  return "successful"
      
  
