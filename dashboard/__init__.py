from flask import Blueprint

dashboard_blueprint=Blueprint('dashboard',__name__)

from .routes import *