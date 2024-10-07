from flask import request, jsonify
from caching import cache
from utils.util import token_required
from marshmallow import ValidationError

from models.schemas.roleSchema import role_schema,roles_schema

from services import roleService

from utils.util import token_required,role_required

# token and or role is needed for each endpoint validating access to each endpoint

# Controllers validates and serializes information for and from requests sent to the API

# creating a role from json data sent to the API using endpoint associated
# admin required
@token_required
@role_required('admin')
def save():
  try:
    role_data = role_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    role_save = roleService.save(role_data)
    return role_schema.jsonify(role_save),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400

# finding all roles using endpoint associated
# admin required
@cache.cached(timeout=60)
@token_required
@role_required('admin')
def find_all():
  roles = roleService.find_all()
  return roles_schema.jsonify(roles), 200

# updating a role from json data sent to the API using endpoint associated
# admin required
@token_required
@role_required('admin')
def update(id):
  try:
    role_data = role_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages),400
  try:
    updated_role = roleService.update(role_data,id)
    return role_schema.jsonify(updated_role),201
  except ValueError as e:
    return jsonify({"error": str(e)}),400