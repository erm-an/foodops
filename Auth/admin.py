from flask.ext import admin
from flask.ext import login
from flask.ext.admin.contrib import sqla
from models import User

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated()


# Create customized index view class
class MyAdminIndexView(admin.AdminIndexView):
    def is_accessible(self):
        return login.current_user.is_authenticated()

def init_admin_view(app, db):
    flask_admin = admin.Admin(app, 'Auth', index_view=MyAdminIndexView())
    flask_admin.add_view(MyModelView(User, db.session))
