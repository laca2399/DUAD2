from flask import Flask
from users import users_bp 
from products import products_bp 
from sales import sales_bp 
from jwt_manager import JWT_Manager  

app = Flask(__name__)
jwt_manager = JWT_Manager()

from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")


app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(sales_bp, url_prefix='/sales')

@app.route("/liveness")
def liveness():
    return "<p>API is alive!</p>"

if __name__ == "__main__":
    app.run(debug=True)
