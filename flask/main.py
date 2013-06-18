# –*- encoding:utf8 –*-
from flask import Flask, url_for, redirect, render_template, request, make_response, session
import urllib2
import uuid
import json
import config
import db

app = Flask(__name__)
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('../logs/app.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

@app.route('/')
def index():
    uid = request.cookies.get('uid')

    user = None
    if uid:
        conn = db.get_conn()
        user_key = 'user:{uid}'.format(uid=uid)
        user = conn.hgetall(user_key)

    return render_template('index.html', conf=config, user=user)

@app.route('/login', methods=['POST'])
def login():
    source = request.form['source']
    platform_uid = request.form['platform_uid']
    access_token = request.form['access_token']

    # Get user data from platform.
    platform_url = 'https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}' \
        .format(access_token=access_token, uid=platform_uid)
    platform_res = urllib2.urlopen(platform_url)
    platform_res_body = platform_res.read()
    platform_user = json.loads(platform_res_body)

    if platform_user is None or 'screen_name' not in platform_user:
        return ''

    pid = '{source}_{platform_uid}'.format(source=source, platform_uid=platform_uid)
    pid_uid_key = 'platform_uid:{pid}:uid'.format(pid=pid)

    conn = db.get_conn()
    uid = conn.get(pid_uid_key)
    if uid == None:
        uid = str(uuid.uuid1()).upper()
        conn.set(pid_uid_key, uid)

    user_key = 'user:{uid}'.format(uid=uid)

    pipe = conn.pipeline()
    pipe.hset(user_key, 'source', source)
    pipe.hset(user_key, 'platform_uid', platform_uid)
    pipe.hset(user_key, 'access_token', access_token)
    pipe.hset(user_key, 'name', platform_user['screen_name'])
    pipe.execute()

    # Storing cookies.
    resp = make_response()
    resp.set_cookie('uid', uid, max_age=864000)
    return resp

@app.route('/wb_callback')
def weibo_callback():
    return render_template('weibo_callback.html')


if __name__ == "__main__":
    #app.debug = True
    app.run()