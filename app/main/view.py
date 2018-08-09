"""
    Created by zltningx on 18-4-28.
"""

from flask import request, render_template, \
    redirect, session, url_for, flash, send_from_directory
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from .form import LoginForm, SearchForm
from . import main
from ..models import Admin, Task, Plugin
from ..utils import ip_recognize, gen_recommend, dump, load
from .. import db
from ..decorators import login_required

from redis import Redis
import os

redis = Redis("127.0.0.1")
directory = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "download")


@main.route("/", methods=['GET', 'POST'])
# @login_required
def index():
    form = SearchForm()
    if form.validate_on_submit():
        ip_list = ip_recognize(form.ip.data)
        port_list = form.port.data.split(',')
        if form.port.data:
            for port in port_list:
                if not port.isdigit():
                    flash("端口格式错误")
                    return redirect(url_for('.index'))
        else:
            port_list = list()
        task = Task(ip_list=ip_list, port_list=port_list)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for(".task_detail", task_id=task.id))
    return render_template('index.html', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.\
            filter_by(admin_username=form.admin.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            flash("welcome! {}".format(admin.admin_username))
            return redirect(url_for('.index'))
        flash("错误的用户名或密码 ！")
    return render_template('login.html', form=form)


@main.route('/advance', methods=['GET', 'POST'])
# @login_required
def advance():

    return render_template("advance.html")


@main.route('/task', methods=['GET', 'POST'])
# @login_required
def task():
    tasks = Task.query.all()
    return render_template("task.html", tasks=tasks)


@main.route('/task/<int:task_id>', methods=['GET', 'POST'])
# @login_required
def task_detail(task_id):
    task = Task.query.filter_by(id=task_id).first()
    check_list = request.form.getlist('check')
    submit = request.form.get('submit')
    if check_list and submit:
        for plugin in task.plugins:
            task.delete_plugin(plugin.plugin_filename)
        for name in check_list:
            task.add_plugin(name)
        task.active = True
        return redirect(url_for(".running_detail", task_id=task.id))
    elif submit:
        task.active = False
        for plugin in task.plugins:
            task.delete_plugin(plugin.plugin_filename)

    plugins = Plugin.query.all()
    remain_plugins = list()
    if task.port_list:
        recommend_plugins = gen_recommend(task.port_list)
        for plugin in plugins:
            if plugin not in recommend_plugins:
                remain_plugins.append(plugin)
    else:
        recommend_plugins = plugins
    return render_template("task_detail.html", task=task,
                           recommend_plugins=recommend_plugins,
                           remain_plugins=remain_plugins)


@main.route('/running', methods=['GET', 'POST'])
# @login_required
def running():
    tasks = Task.query.filter_by(active=True)
    for task in tasks:
        if not redis.get(task.id):
            task.active = False
    tasks = Task.query.filter_by(active=True)
    a = redis.lrange("1-result", 0, redis.llen("1-result"))
    return render_template("running.html", tasks=tasks)


@main.route('/running/<task_id>', methods=['GET', 'POST'])
# @login_required
def running_detail(task_id):
    task = Task.query.filter_by(id=task_id).first()
    running_task = redis.get(task_id)
    if not running_task:
        plugins = list()
        for plugin in task.plugins:
            plugins.append(plugin.plugin_name)
        executor = ThreadPoolExecutor(1)
        redis.set(task_id, 'start')
        executor.submit(run_plugin, plugins,
                        task.ip_list, task.port_list, task_id)
        return redirect(url_for(".running"))
    else:
        task.active = False
        return redirect(url_for(".running"))
    # return render_template("running_detail.html", task=task)


@main.route('/cancel/<task_id>', methods=['GET', 'POST'])
# @login_required
def cancel(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.active = False
    redis.delete(task_id)
    return redirect(url_for('.running'))


def run_plugin(plugins, ip_list, port_list, task_id):

    for plugin in plugins:
        if redis.get(task_id):
            try:
                from importlib import import_module
                tmp_module = import_module(".plugin.plugins."+plugin, 'app')
                result = tmp_module.run(plugin, ip_list, port_list)
                redis.lpush(str(task_id) + '-result', dump(result))
            except Exception as e:
                print(e)
        else:
            break

    # store as file
    rst = redis.lrange(task_id + "-result", 0,
                       redis.llen(task_id+ "-result"))
    try:
        with open(directory + "/" + task_id + '-result.mydb', 'wb') as f:
            f.write(dump(rst))
    except Exception as e:
        print(e)
    redis.delete(task_id)


@main.route('/statistic', methods=['GET', 'POST'])
# @login_required
def statistic():
    tasks = Task.query.filter_by(active=False)
    return render_template("statistic.html", tasks=tasks)


@main.route('/statistic/<task_id>', methods=['GET', 'POST'])
def statistic_detail(task_id):
    result = list()
    rst = redis.lrange("1-result", 0, redis.llen("1-result"))
    if not rst:
        with open(directory + '/' + task_id + '-result.mydb', 'rb') as f:
            rst = load(f.read())
    for i in rst:
        result.append(load(i))
    if 0:
        return redirect(url_for(".download", filename=task_id+'-result.mydb'))
    return render_template('statistic_detail.html', result=result)


@main.route('/download/<filename>', methods=['GET',])
def download(filename):

    return send_from_directory(directory, filename, as_attachment=True)
