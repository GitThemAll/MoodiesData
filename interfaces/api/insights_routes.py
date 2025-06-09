from fastapi import APIRouter, Query
from flask import Blueprint, jsonify, request
from application.services.insights_service import DiscountCodeService

insights_bp = Blueprint('discount_code', __name__)
service = DiscountCodeService()

@insights_bp.route('/discount-metrics', methods=['GET'])
def get_discount_metrics():
    metrics = service.get_discount_code_usage_metrics()
    return jsonify(metrics)


#this function will check orders for certain insights between two dates
# @insights_bp.route("/shopify/discount-revenue", methods=["GET"])
# def discount_revenue():
#     start = request.args.get("start")
#     end = request.args.get("end")

#     if not start or not end:
#         return jsonify({
#             "status": "error",
#             "message": "Missing 'start' or 'end' query parameters"
#         }), 400

#     result = service.get_discount_code_revenue(start, end)
#     return jsonify(result)

@insights_bp.route("/shopify/discount-revenue", methods=["GET"])
def discount_revenue():
    result = service.get_discount_code_revenue()
    return jsonify(result)

#shopify route 
@insights_bp.route("/shopify/discount-order-count", methods=["GET"])
def discount_order_count():
    return jsonify(service.get_discount_code_order_count())