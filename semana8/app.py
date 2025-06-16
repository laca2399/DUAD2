from flask import Flask
from database import db
from models import Base
from users import app as users_bp
from products import app as products_bp
from sales import app as sales_bp
from cache_instance import cache_manager

app = Flask(__name__)

app.cache = cache_manager

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(sales_bp, url_prefix='/sales')

@app.route("/liveness")
def liveness():
    return "<p>API is alive!</p>"

if __name__ == "__main__":
    app.run(debug=True)