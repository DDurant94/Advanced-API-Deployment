from flask import Blueprint
from controllers.orderController import save,find_by_id,find_all

# all the endpoints for orders
order_blueprint = Blueprint('order_bp',__name__)
order_blueprint.route("/add-order",methods=['POST'])(save)
order_blueprint.route("/",methods=["GET"])(find_all)
order_blueprint.route('/id/<int:id>',methods=['GET'])(find_by_id)