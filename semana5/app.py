from flask import Flask
from cars import cars_bp  
from users import users_bp
from rentals import rentals_bp

app = Flask(__name__)


app.register_blueprint(cars_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(rentals_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
