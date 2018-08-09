"""
    Created by zltningx on 18-4-29.
"""

from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


@main.app_errorhandler(403)
def page_forbidden(error):
    return render_template('403.html')
