from flask import Blueprint, jsonify, request
from application.services.insights_service import DiscountCodeService
from application.services.get_top_sku_stats import SkuStatsService

insights_bp = Blueprint('discount_code', __name__)
service = DiscountCodeService()
service_skus = SkuStatsService()

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

#used method to get shopify skus revenu
# @insights_bp.route("/shopify/sku-revenue", methods=["GET"])
# def sku_revenue():
#     start = request.args.get("start")
#     end = request.args.get("end")

#     if not start or not end:
#         return jsonify({"status": "error", "message": "Missing 'start' or 'end'"}), 400

#     return jsonify(service_skus.get_revenue_per_sku(start, end))

@insights_bp.route("/shopify/sku-revenue", methods=["GET"])
def sku_revenue_file():
    result = service_skus.get_revenue_per_sku()
    return jsonify(result)

#used method to get shopify skus order count
# @insights_bp.route("/shopify/sku-order-count", methods=["GET"])
# def sku_order_count():
#     start = request.args.get("start")
#     end = request.args.get("end")

#     if not start or not end:
#         return jsonify({
#             "status": "error",
#             "message": "Missing 'start' or 'end' query parameters"
#         }), 400

#     return jsonify(service_skus.get_order_count_per_sku(start, end))

@insights_bp.route("/shopify/sku-order-count", methods=["GET"])
def sku_order_count_from_file():
    result = service_skus.get_order_count_per_sku()
    return jsonify(result)
