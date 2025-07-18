from flask import Flask
from db.database import db
from db.models import Base
from api.products import  products_bp
from api.sales import sales_bp
from api.users import users_bp
from caches.cache_instance import cache_manager

app = Flask(__name__)

app.cache = cache_manager

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(sales_bp, url_prefix='/sales')

@app.route("/Pet Ecommerce")
def liveness():
    return "<p>Welcome to Pet Ecommerce!</p>"

if __name__ == "__main__":
    app.run(debug=True)
