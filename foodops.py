from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask.ext.socketio import SocketIO

from Auth import init_login 
from Auth.admin import init_admin_view
from Auth.views import create_auth_views
from Auth import models
from shared.models import db

import views

def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    
    db.init_app(app)
    init_login(app)
    init_admin_view(app, db)
    with app.app_context():
        db.create_all()

    main_view = views.create_views()
    app.register_blueprint(url_prefix = '/', blueprint = main_view)   
   
    socketio = SocketIO(app)
    socketio.run(app, '0.0.0.0', 8080)

if __name__ == '__main__':
    main()
