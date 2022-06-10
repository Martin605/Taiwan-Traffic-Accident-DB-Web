from flask import render_template, flash, redirect, url_for, request, jsonify
from app.main import bp
from app.db import DB

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')