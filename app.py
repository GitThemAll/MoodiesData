from flask import Flask
from interfaces.api.user_controller import user_bp
from interfaces.api.discount_code_routes import discount_code_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.register_blueprint(discount_code_bp, url_prefix='/api')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)