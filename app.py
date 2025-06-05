from flask import Flask
from interfaces.api.user_controller import user_bp
from interfaces.api.discount_code_routes import discount_code_bp
from infra.clients.shopify import ShopifyClient
from infra.clients.klaviyo import KlaviyoClient
from application.services.segment_service import segment_service

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(discount_code_bp, url_prefix='/api')
    # client = ShopifyClient()
    # client.get_all_orders_since("2024-03-01T00:00:00Z", output_file="shopify_orders_from_mar_2024.csv")

    # client = KlaviyoClient()
    # profiles = client.fetch_all_profiles()
    # client.save_profiles_to_csv(profiles, filename="klaviyo_customers.csv")

    seg_service = segment_service()
    seg_service.clean_data_static()
    seg_service.feature_data_static()


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)