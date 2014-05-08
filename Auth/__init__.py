from flask import redirect, url_for
from flask.ext import login
from shared.models import db
from models import User
 
def login_required_cb():
    return redirect(url_for('auth.login_view'))

# Initialize flask-login
def init_login(app):
    login_manager = login.LoginManager()
    login_manager.setup_app(app)
    login_manager.unauthorized_handler(login_required_cb)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)
