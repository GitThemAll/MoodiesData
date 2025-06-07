from flask import Flask
from interfaces.api.user_routes import user_bp
from interfaces.api.discount_code_routes import discount_code_bp
from infra.clients.shopify import ShopifyClient
from infra.clients.klaviyo import KlaviyoClient
from application.services.segment_service import segment_service
from flask import Flask
from infra.repositories.users_database import db
import os 

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(discount_code_bp, url_prefix='/api')
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


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


def get_database_path(filename: str = "mydatabase.db") -> str:
    """
    Returns the absolute path to the SQLite database file,
    stored in the 'resources/data' folder.
    Ensures the folder exists.

    :param filename: The database filename (default: 'mydatabase.db')
    :return: Absolute file path to use in SQLAlchemy URI
    """
    folder = os.path.join("resources", "data")
    os.makedirs(folder, exist_ok=True)
    return os.path.abspath(os.path.join(folder, filename))