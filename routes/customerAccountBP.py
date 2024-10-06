from flask import Blueprint
from controllers.customerAccountController import save,find_all,login,find_by_id,update,delete

# all the url endpoints for customer accounts
customer_account_blueprint = Blueprint('customer_account_bp',__name__)
customer_account_blueprint.route('/create-account',methods=['POST'])(save)
customer_account_blueprint.route('/',methods=['GET'])(find_all)
customer_account_blueprint.route('/login',methods =['POST'])(login)
customer_account_blueprint.route('/id/<int:id>',methods=['GET'])(find_by_id)
customer_account_blueprint.route('/update/id/<int:id>', methods=['PUT'])(update)
customer_account_blueprint.route('/delete/id/<int:id>',methods=['DELETE'])(delete)