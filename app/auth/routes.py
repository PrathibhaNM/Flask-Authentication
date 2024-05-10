from flask import request, session,redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from app.auth import auth_blueprint
from flask_bcrypt import generate_password_hash,check_password_hash

@auth_blueprint.route('/login',methods=['GET','POST'])
def login():
    from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
    from app import users_collection
    from flask_bcrypt import generate_password_hash,check_password_hash
    
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

@auth_blueprint.route('/logout',methods=['POST'])
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



@auth_blueprint.route('/register',methods=['GET','POST'])
def register():
    from app import users_collection
    from flask_bcrypt import generate_password_hash,check_password_hash
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
