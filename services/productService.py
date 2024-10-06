from sqlalchemy.orm import Session
from database import db
from sqlalchemy import select

from models.product import Product
from models.order import Order
from models.orderProduct import OrderProducts

# Adding product to database
def save(product_data):
  with Session(db.engine) as session:
    with session.begin():
      new_product = Product(name=product_data['name'], price=product_data['price'], quantity=product_data['quantity'], description=product_data['description'])
      session.add(new_product)
      session.commit()
    session.refresh(new_product)
    return new_product

# Getting all products with pagination
def find_all(page=1,per_page=10):
  products = db.paginate(select(Product),page=page,per_page=per_page)
  return products

def find_by_id(id):
  query = select(Product).filter_by(id=id)
  product = db.session.execute(query).unique().scalar_one_or_none()
  return product

# updating a products information
def update(product_data, id):
  with Session(db.engine) as session:
    with session.begin():
      product = db.session.execute(db.select(Product).where(Product.id == id)).unique().scalar_one_or_none()
      product.id = product_data['id']
      product.name = product_data['name']
      product.price = product_data['price']
      product.quantity = product_data['quantity']
      product.description = product_data['description']
    db.session.commit()
  return product

# deleting a product and associations
def delete(id):
  with Session(db.engine) as session:
    with session.begin():
      product = session.execute(db.select(Product).where(Product.id == id)).unique().scalar_one_or_none()
      if product is None:
          return None
      order_items = session.execute(db.select(OrderProducts).where(OrderProducts.product_id == id)).scalars().all()

      for item in order_items:
        session.delete(item)
          
      for item in order_items:
        order_id = item.order_id
        remaining_items = session.execute(db.select(OrderProducts).where(OrderProducts.order_id == order_id)).scalars().all()
        
        if not remaining_items:
          order = session.execute(db.select(Order).where(Order.id == order_id)).unique().scalar_one_or_none()
          if order:
            session.delete(order)
          
      session.delete(product)
    session.commit()
  return "successful"