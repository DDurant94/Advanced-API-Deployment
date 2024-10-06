from flask import request, jsonify
from models.schemas.orderSchema import order_schema,orders_schema,order_schema_customer
from services import orderService
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

# token and or role is needed for each endpoint validating access to each endpoint

# Controllers validates and serializes information for and from requests sent to the API

# creating a order from json data sent to the API using endpoint associated
@token_required
def save():
  try:
    order_data = order_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  
  try:
    order_save = orderService.save(order_data)
    return order_schema.jsonify(order_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400

# getting all orders
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
  page = request.args.get('page',1,type=int)
  per_page=request.args.get('per_page',10,type=int)
  return orders_schema.jsonify(orderService.find_all(page=page,per_page=per_page)),200

# getting orders by id
@cache.cached(timeout=60)
@token_required
def find_by_id(id):
  order= orderService.find_by_id(id)
  return order_schema_customer.jsonify(order),200