from flask import Flask, request, session, redirect, url_for, flash, make_response
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
#import requests
# from flask_bcrypt import generate_password_hash,check_password_hash
from app.config import SECRET_KEY, MONGODB_URL, JWT_SECRET_KEY

# Creating the instance of Flask class
app = Flask(__name__)
app.config.from_pyfile('config.py')


jwt = JWTManager(app)

app.secret_key = SECRET_KEY  # Used to encrypt session data
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Add your MongoDB URL here
# dbURL=''

dbURL = MONGODB_URL
client = MongoClient(dbURL)
db = client['flask_user_authentication']
users_collection = db['users']


# Function to add access token to request headers before each request
# @app.before_request
# def add_access_token_to_header():
#     # Check if the user is logged in (you may implement your own logic here)
#     if session.get('logged_in'):
#         # Add the access token to the request headers
#         access_token = session.get('access_token')
#         if access_token:
#             # Create a new dictionary with the additional header
#             headers = dict(request.headers)
#             headers['Authorization'] = f'Bearer {access_token}'
#             request.environ['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'


from app.auth.routes import auth_blueprint
from app.dashboard.routes import dashboard_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)

# if __name__ == '__main__':
#     app.run(debug=True)





