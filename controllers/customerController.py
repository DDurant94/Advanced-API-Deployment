from flask import request, jsonify
from models.schemas.customerSchema import customer_schema,customers_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

# token and or role is needed for each endpoint validating access to each endpoint

# Controllers validates and serializes information for and from requests sent to the API

# creating a customer from json data sent to the API using endpoint associated
# admin required
@token_required
@role_required('admin')
def save():
  try:
    customer_data = customer_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  
  customer_save = customerService.save(customer_data)
  if customer_save is not None:
    return customer_schema.jsonify(customer_save),201
  else:
    return jsonify({"message": "Fallback method error activated", "body":customer_data}), 400

# getting all customers
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
  customers = customerService.find_all()
  if customers:
    return customers_schema.jsonify(customers), 200
  else:
    resp={
      "status":"Error",
      "message": "No Customers In Database"
    }
    return jsonify(resp), 400

# getting all customers pagination
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all_pagination():
  page=request.args.get('page',1,type=int)
  per_page= request.args.get('per_page',10,type=int)
  customers = customerService.find_all_pagination(page=page,per_page=per_page)
  if customers:
    return customers_schema.jsonify(customers), 200
  else:
    resp={
      "status":"Error",
      "message": "No Customers In Database"
    }
    return jsonify(resp), 400

# getting customers by id
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_by_id(id):
  customer = customerService.find_by_id(id)
  return customer_schema.jsonify(customer),200

# updating a customer from json data sent to the API using endpoint associated
# admin required 
@token_required
@role_required('admin')
def update(id):
  try:
    customer_data = customer_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    updated_customer = customerService.update(customer_data,id)
    return customer_schema.jsonify(updated_customer),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400  

# deleting a customer 
# admin required 
@token_required
@role_required('admin')
def delete(id):
  customer = customerService.delete(id)
  if customer == "successful":
    return jsonify({"message": "Customer removed successfully"}), 200
  else:
    return jsonify({"message": f"Couldn't find customer with ID {id}"}), 404 