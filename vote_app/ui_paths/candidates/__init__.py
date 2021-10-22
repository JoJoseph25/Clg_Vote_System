from flask import Blueprint

candi = Blueprint('candi', __name__)

from . import views