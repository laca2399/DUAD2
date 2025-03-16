from flask import Flask
from products import app as products_app
from sales import app as sales_app
from users_and_authentication import app as auth_app

def create_app():
    app = Flask(__name__)

    app.register_blueprint(products_app, url_prefix='/products')
    app.register_blueprint(sales_app, url_prefix='/sales')
    app.register_blueprint(auth_app, url_prefix='/auth')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
