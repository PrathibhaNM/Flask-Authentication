from flask import request, session,redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from app.dashboard import dashboard_blueprint
from flask_bcrypt import generate_password_hash,check_password_hash

@dashboard_blueprint.route('/')
def dashboard():
    return redirect(url_for('auth.login'))


@dashboard_blueprint.route('/userDashboard')
@jwt_required()
def userDashboard():
    current_user = get_jwt_identity()
    print(current_user)
    logout_button = '<form method="POST" action="/logout"><button type="submit">Logout</button></form>'
    welcome_message = f'<p>Welcome, {current_user}</p>'
    logout_form = f'<p>{logout_button}</p>'
    return welcome_message + logout_form

