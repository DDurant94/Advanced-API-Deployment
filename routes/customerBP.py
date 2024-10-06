from flask import Blueprint
from controllers.customerController import save, find_all,find_by_id,update,delete,find_all_pagination

# all the endpoints for customers
customer_blueprint = Blueprint('customer_bp',__name__)
customer_blueprint.route('/add-customer',methods=['POST'])(save)
customer_blueprint.route('/',methods=['GET'])(find_all_pagination)
customer_blueprint.route('/id/<int:id>',methods=['GET'])(find_by_id)
customer_blueprint.route('/update/id/<int:id>', methods=['PUT'])(update)
customer_blueprint.route('/delete/id/<int:id>',methods=['DELETE'])(delete)
