from flask import Blueprint

choose = Blueprint('choose', __name__)

from . import views
from . import forms