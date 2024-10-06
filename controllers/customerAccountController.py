from flask import request, jsonify
from models.schemas.customerAccountSchema import customer_account_schema,customer_accounts_schema,add_customer_account_schema
from services import customerAccountService
from marshmallow import ValidationError
from caching import cache
from utils.util import token_required, role_required

# token and or role is needed for each endpoint validating access to each endpoint

# Controllers validates and serializes information for and from requests sent to the API

# creating a customer account from json data sent to the API using endpoint associated
# admin required
@token_required
@role_required('admin')
def save():
  try:
    customer_account_data = add_customer_account_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    customer_account_save = customerAccountService.save(customer_account_data)
    return add_customer_account_schema.jsonify(customer_account_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400


# getting all customer accounts 
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
  customer_accounts = customerAccountService.find_all()
  return customer_accounts_schema.jsonify(customer_accounts),200

# logging into an account
@cache.cached(timeout=60)
def login():
  customer = request.json
  user = customerAccountService.login_customer(customer['username'], customer['password'])
  if user:
    return jsonify(user),200
  else:
    resp={
      "status":"Error",
      "message": "User does not exist"
    }
    return jsonify(resp), 400


# getting account by id
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_by_id(id):
  customer = customerAccountService.find_by_id(id)
  return customer_account_schema.jsonify(customer),200


# updating a customer account from json data sent to the API using endpoint associated
# admin required 
@token_required
@role_required('admin')
def update(id):
  try:
    customer_data = add_customer_account_schema.load(request.json)
    print(customer_data)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    updated_customer = customerAccountService.update(customer_data,id)
    return add_customer_account_schema.jsonify(updated_customer),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400

# deleting customer account
# admin required
@token_required
@role_required('admin')
def delete(id):
  customer = customerAccountService.delete(id)
  if customer == "successful":
    return jsonify({"message": "Customer removed successfully"}), 200
  else:
    return jsonify({"message": f"Couldn't find customer with ID {id}"}), 404 