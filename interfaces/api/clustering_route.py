from flask import Blueprint, jsonify
from application.services.dbscan_service import dbscan_service

clustering_bp = Blueprint('clustering', __name__)
service = dbscan_service()

@clustering_bp.route('/train-clustering', methods=['POST'])
def train_clustering_model():
    result = service.train_model()
    return jsonify(result)