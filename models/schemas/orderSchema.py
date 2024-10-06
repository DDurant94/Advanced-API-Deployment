from marshmallow import fields
from schema import ma

# Validation of data 

# Order schema
class OrderSchema(ma.Schema):
  id = fields.Integer(required=False)
  date = fields.Date(required=True)
  customer_id = fields.Integer(required=True)
  products = fields.List(fields.Nested(lambda:OrderProductSchema), required=True)
  


# Order Product schema holds all information associated with the product of an order
class OrderProductSchema(ma.Schema):
  product_id = fields.Integer(required=True)
  quantity = fields.Integer(required=True)
  product = fields.Nested('ProductSchema')
  
# Order Product schema holds all information associated with the product and customer of an order
class OrderSchemaCustomer(ma.Schema):
  id = fields.Integer(required=False)
  date = fields.Date(required=True)
  customer = fields.Nested('CustomerSchema')
  products = fields.Nested('ProductSchema',many=True)
  
order_schema_customer = OrderSchemaCustomer()
  
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)