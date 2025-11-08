"""
Main controller for home and general pages
"""
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
