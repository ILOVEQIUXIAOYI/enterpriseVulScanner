"""
    Created by zltningx on 18-4-28.
"""

from flask import Blueprint

main = Blueprint("main", __name__)

from . import view, errors
