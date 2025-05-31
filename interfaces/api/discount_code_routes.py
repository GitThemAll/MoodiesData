from flask import Blueprint, jsonify
from application.services.discount_code_service import DiscountCodeService

discount_code_bp = Blueprint('discount_code', __name__)
service = DiscountCodeService()

@discount_code_bp.route('/discount-metrics', methods=['GET'])
def get_discount_metrics():
    metrics = service.get_discount_code_usage_metrics()
    return jsonify(metrics)