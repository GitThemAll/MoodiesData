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