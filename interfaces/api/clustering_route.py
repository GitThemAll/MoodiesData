from flask import Blueprint, jsonify
from application.services.dbscan_service import dbscan_service

clustering_bp = Blueprint('clustering', __name__)
service = dbscan_service()

@clustering_bp.route('/train-clustering', methods=['POST'])
def train_clustering_model():
    result = service.train_model()
    return jsonify(result)

@clustering_bp.route("/dbscan-summary", methods=["GET"])
def dbscan_summary():
    result = service.get_cluster_summary_json()
    return jsonify(result)

@clustering_bp.route("/distribution", methods=["GET"])
def cluster_distribution():
    result = service.get_cluster_distribution_summary()
    return jsonify(result)

@clustering_bp.route("/items-per-cluster", methods=["GET"])
def items_per_cluster():
    result = service.get_avg_items_per_cluster()
    return jsonify(result)

@clustering_bp.route("/city-distribution", methods=["GET"])
def cluster_by_city():
    result = service.get_cluster_distribution_by_city()
    return jsonify(result)

@clustering_bp.route("/country-distribution", methods=["GET"])
def cluster_by_country():
    result = service.get_cluster_distribution_by_country()
    return jsonify(result)

@clustering_bp.route("/clustering-cards-metrics", methods=["GET"])
def cluster_metrics():
    result = service.get_cluster_dashboard_cards()
    return jsonify(result)