from flask import Flask, request, session, redirect, url_for, flash, make_response
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import requests
from flask_bcrypt import generate_password_hash,check_password_hash
from settings import SECRET_KEY, MONGODB_URL, JWT_SECRET_KEY

# Creating the instance of Flask class
app = Flask(__name__)

app.secret_key = SECRET_KEY  # Used to encrypt session data
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

jwt = JWTManager(app)

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


# Route for Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'],password):
            access_token = create_access_token(identity=username)
            session['logged_in'] = True
            session['access_token'] = access_token
            return {'access_token': access_token}, 200
            #return redirect('/userDashboard')
            #return redirect(url_for('userDashboard'))
        else:
            return '''
            <p>Invalid username or password</p>
            <p> <a href="/login">Try again</a> </p>
            '''
        
    return '''
        <form method="post">
            <h2>Login here</h2>
            <p>
                <label for="name">Username</label>
                <input type="text" id="name" name="username">
            </p>
            <p>
                <label for="password">Password</label>
                <input type="password" name="password">
            </p>
            <p><input type="submit" value="Login"></p>
            
        </form>
        <p>Don't have an account? <a href="/register">Register here</a></p>
    '''


# Root/Home route
@app.route('/')
def dashboard():
    return redirect(url_for('login'))


@app.route('/userDashboard')
@jwt_required()
def userDashboard():
    current_user = get_jwt_identity()
    print(current_user)
    logout_button = '<form method="POST" action="/logout"><button type="submit">Logout</button></form>'
    welcome_message = f'<p>Welcome, {current_user}</p>'
    logout_form = f'<p>{logout_button}</p>'
    return welcome_message + logout_form
    

# Route for LogOut
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    session.clear()
    return '''
    <p> <h2>Successfully Logged out</h2> </p> 
    <p>   
        <button type="button">
            <a href="/login">LogIn</a>
        </button>
    </p>

    '''


# Route for Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Hashing the password
        hashed_password = generate_password_hash(password).decode('utf-8')

        #Checking if username already exists in the database
        user = users_collection.find_one({'username': username})

        if user:
            return 'Username already exists. Please choose a different username.'
        else:
            #Insert the user into the database
            users_collection.insert_one({'username': username, 'password': hashed_password})
            return '''
            <p>Registration successful.</p>
            <p>You can now <a href="/login">login</a> with your new account.</p>'''
    return '''
        <form method="post">
            <p>
                <label for="name">Username</label>
                <input type="text" name="username" placeholder="Username">
            </p>
            <p>
                <label for="password">Username</label>
                <input type="password" name="password" placeholder="Password">
            </p>
            <p><input type="submit" value="Register"></p>
        </form>
    '''


# if __name__ == '__main__':
#     app.run(debug=True)





