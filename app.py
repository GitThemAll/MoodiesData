from flask import Flask
from interfaces.api.user_controller import user_bp
from interfaces.api.discount_code_routes import discount_code_bp
from infra.clients.shopify import ShopifyClient

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(discount_code_bp, url_prefix='/api')
    client = ShopifyClient()
    client.get_all_orders_since("2024-03-01T00:00:00Z", output_file="shopify_orders_from_mar_2024.csv")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)