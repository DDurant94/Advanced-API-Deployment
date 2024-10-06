from marshmallow import fields, validate
from schema import ma

# Validation of data 

# Product schema
class ProductSchema(ma.Schema):
  id = fields.Integer(required=False)
  name = fields.String(required=True, validate=validate.Length(min=1))
  price = fields.Float(required=True, validate=validate.Range(min=0))
  quantity = fields.Integer(required=True, validate=validate.Range(min=0))
  description = fields.String(required=True, validate=validate.Length(min=1))


# Product ID schema to get just the ID of a product
class ProductSchemaId(ma.Schema):
  id = fields.Integer(required=True)
    
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)