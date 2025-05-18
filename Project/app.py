from flask import Flask
from database import db
from models import Base
from products import app as products_bp
from sales import app as sales_bp
from users import app as users_bp

app = Flask(__name__)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(sales_bp, url_prefix='/sales')

@app.route("/Pet Ecommerce")
def liveness():
    return "<p>Welcome to Pet Ecommerce!</p>"

if __name__ == "__main__":
    app.run(debug=True)
