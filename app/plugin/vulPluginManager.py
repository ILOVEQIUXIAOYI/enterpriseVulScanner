"""
    Created by zltningx on 18-4-28.
"""

from .. import db
from ..models import Plugin

import os


basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, 'plugins')


class VulPluginManager(object):
    @classmethod
    def init_plugin(cls):
        plugin_names = os.walk(path)
        for r, d, files in plugin_names:
            for file in files:
                if file.split('.')[-1] == 'py':
                    plugin = Plugin(plugin_filename=file)
                    db.session.add(plugin)
        db.session.commit()

    @classmethod
    def update(cls):
        plugin_names = os.walk(path)
        for r, d, files in plugin_names:
            for file in files:
                if not Plugin.query.filter_by(plugin_filename=file).first()\
                        and file.split('.')[-1] == 'py':
                    plugin = Plugin(plugin_filename=file)
                    db.session.add(plugin)
        db.session.commit()

    @classmethod
    def delete(cls, plugin_filename):
        os.rename(os.path.join(path, plugin_filename),
                  os.path.join(path, plugin_filename+'.rm'))