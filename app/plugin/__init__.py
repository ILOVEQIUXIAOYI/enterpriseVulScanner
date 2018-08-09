"""
    Created by zltningx on 18-4-30.
"""
from flask import Blueprint

plugin = Blueprint("plugin", __name__)

from . import view
