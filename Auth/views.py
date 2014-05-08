from flask import Flask, Blueprint, url_for, redirect, render_template, request
from flask.ext import login
from flask.ext.login import logout_user, login_required
from flask.ext.admin import helpers
from forms import LoginForm, RegistrationForm
from shared.models import db
from models import User

def create_auth_views():
    auth_app = Blueprint('auth', __name__)

    @auth_app.route('/')
    def index():
        return render_template('login_page.html', user=login.current_user)

    @auth_app.route('/login', methods=('GET', 'POST'))
    def login_view():
        form = LoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            print(user)
            remember_me = form.remember_me.data
            login.login_user(user, remember=remember_me)
            return redirect('/ui')

        return render_template('login_form.html', form=form)

    @auth_app.route("/logout")
    @login_required
    def logout_view():
        logout_user()
        return redirect(url_for('auth.login_view'))

    return auth_app
