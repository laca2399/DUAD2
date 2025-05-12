from flask import Flask
from sqlalchemy import create_engine
from models import Base
from productsnew import app as products_bp
from salesnew import app as sales_bp
from users import app as users_bp

app = Flask(__name__)
engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")
Base.metadata.create_all(engine)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/productsnew')
app.register_blueprint(sales_bp, url_prefix='/salesnew')

@app.route("/Pet Ecommerce")
def liveness():
    return "<p>Welcome to Pet Ecommerce!</p>"

if __name__ == "__main__":
    app.run(debug=True)
