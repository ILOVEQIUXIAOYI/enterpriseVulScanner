"""
    Created by zltningx on 18-4-30.
"""

from . import plugin
from ..models import Plugin
from .. import db
from .vulPluginManager import VulPluginManager
from flask import render_template, redirect, url_for, flash, g
from ..decorators import login_required


@plugin.route('/plugins', methods=['GET', 'POST'])
# @login_required
def plugins():
    plugins = Plugin.query.all()
    if not plugins:
        VulPluginManager().init_plugin()
        plugins = Plugin.query.all()
    return render_template('plugin_manager.html', plugins=plugins)


@plugin.route('/delete/<plugin_filename>', methods=['GET', 'POST'])
# @login_required
def delete_plugin(plugin_filename):
    plugin = Plugin.query.filter_by(plugin_filename=plugin_filename).first()
    if plugin:
        db.session.delete(plugin)
        db.session.commit()
        VulPluginManager.delete(plugin.plugin_filename)
        flash("插件{}已删除！".format(plugin.plugin_name))
    else:
        flash("插件{}不存在！".format(plugin.plugin_name))
    return redirect(url_for('.plugins'))


@plugin.route('/update', methods=['GET', 'POST'])
# @login_required
def update_plugin_from_local():
    VulPluginManager().update()
    flash("从本地更新成功！")
    return redirect(url_for('.plugins'))
