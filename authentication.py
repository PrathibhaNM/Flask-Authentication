from flask import Flask, request, session, redirect, url_for, flash
from pymongo import MongoClient

# Creating the instance of Flask class
app = Flask(__name__)

app.secret_key = 'mysessionkey'  # Used to encrypt session data

#Add your MongoDB URL here
dbURL = ''
#client = MongoClient('mongodb://localhost:27017/')
client = MongoClient(dbURL)
db = client['flask_user_authentication']
users_collection = db['users']


#Route for Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user :
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
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
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return '''
    <p><h2>Welcome!!</h2></p>
    
    <form method="POST" action ="/logout">
       <p><input type="submit" value="Logout"></p>
    </form>
    
    '''

#Route for LogOut
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return '''
    <p> <h2>Successfully Logged out</h2> </p> 
    <p>   
        <button type="button">
            <a href="/login">LogIn</a>
        </button>
    </p>

    '''

#Route for Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user:
            return 'Username already exists. Please choose a different username.'
        else:
            users_collection.insert_one({'username': username, 'password': password})
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



