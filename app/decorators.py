"""
    Created by zltningx on 18-4-28.
"""

from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("请先登录")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function
