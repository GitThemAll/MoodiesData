from flask import Blueprint, jsonify
from application.services.get_top_sku_stats import SkuStatsService

sku_metrics_bp = Blueprint('sku_metrics', __name__)
service = SkuStatsService()

@sku_metrics_bp.route('/sku-metrics', methods=['GET'])
def get_top_sku_metrics():
    metrics = service.get_top_sku_metrics()
    return jsonify({"status": "success", "data": metrics})