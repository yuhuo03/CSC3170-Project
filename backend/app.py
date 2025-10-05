from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
from flask_restful import Api
from routes import initialize_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

api = Api(app)
initialize_routes(api)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)