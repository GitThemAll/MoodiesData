from flask import Blueprint
from application.services.npd_service import NPDService

npd_blueprint = Blueprint('npd', __name__)
npd_service = NPDService()

@npd_blueprint.route('/npd-predictions', methods=['GET'])
def get_customer_predictions():
    customers_predictions = npd_service.get_customer_predictions()
    return customers_predictions

@npd_blueprint.route("/npd-stats", methods=["GET"])
def get_next_purchase_stats():
    return npd_service.get_customer_statistics()