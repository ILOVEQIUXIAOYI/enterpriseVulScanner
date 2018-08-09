"""
    Created by zltningx on 18-4-29.
"""

from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from importlib import import_module
from datetime import datetime


class Admin(UserMixin, db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)

    def __repr__(self):
        return "<Admin: {}>".format(self.admin_username)

    @property
    def password(self, password):
        raise AttributeError("password can't be read.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def is_authenticated(self):
    #     return True

registrations = db.Table('registrations',
    db.Column('plugin_id', db.Integer, db.ForeignKey('plugin.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
)


class Plugin(db.Model):
    __tablename__ = "plugin"
    id = db.Column(db.Integer, primary_key=True)
    plugin_filename = db.Column(db.String(30), unique=True, index=True)

    def __repr__(self):
        return self.plugin_filename

    @property
    def plugin_name(self):
        return self.plugin_filename.split('.')[0]

    @property
    def description_name(self):
        res_tmp = import_module(".plugin.plugins." + self.plugin_name, 'app')
        return res_tmp.plugin_info()['name']

    def get_plugin_info(self):
        res_tmp = import_module(".plugin.plugins." + self.plugin_name, 'app')
        return res_tmp.plugin_info()

    def get_recommend_port(self):
        res_tmp = import_module(".plugin.plugins." + self.plugin_name, 'app')
        return res_tmp.recommend_port

    def run(self, ip_list, port_list):
        res_tmp = import_module(".plugin.plugins." + self.plugin_name, 'app')
        return res_tmp.run(ip_list, port_list)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=False, index=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    ip_list = db.Column(db.PickleType, nullable=False)
    port_list = db.Column(db.PickleType, nullable=True)
    plugins = db.relationship("Plugin", secondary=registrations,
                              backref=db.backref("plugin", lazy="dynamic"),
                              lazy="dynamic")

    @property
    def task_id(self):
        return self.id

    def is_active(self):
        return self.active

    def add_plugin(self, name):
        plugin = Plugin.query.filter_by(plugin_filename=name+'.py').first()
        if plugin:
            self.plugins.append(plugin)
            db.session.add(self)

    def delete_plugin(self, name):
        plugin = Plugin.query.filter_by(plugin_filename=name).first()
        self.plugins.remove(plugin)
        db.session.add(self)