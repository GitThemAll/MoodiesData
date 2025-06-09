from flask import Flask
from flask_cors import CORS
from interfaces.api.user_routes import user_bp
from interfaces.api.insights_routes import insights_bp
from interfaces.api.clustering_route import clustering_bp
from interfaces.api.sku_metrics_routes import sku_metrics_bp
from interfaces.api.clv_route import clv_bp
from infra.clients.shopify import ShopifyClient
from infra.clients.klaviyo import KlaviyoClient
from application.services.segment_service import segment_service
from application.services.dbscan_service import dbscan_service
from flask import Flask
from infra.repositories.users_database import db
import os
from interfaces.api.npd_controller import npd_blueprint 

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])
    #register rooutes
    app.register_blueprint(user_bp)
    app.register_blueprint(insights_bp, url_prefix='/insights')
    app.register_blueprint(clustering_bp, url_prefix="/ml")
    app.register_blueprint(sku_metrics_bp, url_prefix='/insights')
    app.register_blueprint(clv_bp, url_prefix='/clv')

    app.register_blueprint(npd_blueprint)
    db_path = get_database_path()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    
    # client = ShopifyClient()
    # client.get_all_orders_since("2024-03-01T00:00:00Z", output_file="shopify_orders_from_mar_2024.csv")

    # client = KlaviyoClient()
    # profiles = client.fetch_all_profiles()
    # client.save_profiles_to_csv(profiles, filename="klaviyo_customers.csv")

    # seg_service = segment_service()
    # seg_service.clean_data_static()
    # seg_service.feature_data_static()
    # seg_service.train_model()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


def get_database_path(filename: str = "mydatabase.db") -> str:
    """
    Returns the absolute path to the SQLite database file

    :param filename: The database filename (default: 'mydatabase.db')
    :return: Absolute file path to use in SQLAlchemy URI
    """
    folder = os.path.join("resources", "data")
    os.makedirs(folder, exist_ok=True)
    return os.path.abspath(os.path.join(folder, filename))