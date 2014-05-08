from flask import Blueprint, Response, render_template, redirect, request
from flask.ext.login import login_required, current_user

def create_views():
    main_view = Blueprint('main_view', __name__)

    @main_view.route('/', methods = ['GET'])
    #@login_required
    def index():
       	return redirect("http://www.google.com", code=302)#render_template('index.html', user=current_user)


    return main_view
