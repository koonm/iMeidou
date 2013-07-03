# –*- encoding:utf8 –*-
from flask import Flask, url_for, redirect, render_template, request, make_response, session
import os, time, uuid, json
import config
import db

app = Flask(__name__, static_folder='../statics', static_url_path='')
if not app.debug:
    log_dir = '../logs'
    if not os.path.exists(log_dir): os.makedirs(log_dir)
    
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(log_dir + '/app.log')
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
    access_token = request.form['access_token']
    expires_in = request.form['expires_in']

    platform_data = json.loads(request.form['platform_data'])
    if platform_data is None:
        return ''

    platform_user = platform_data['data']
    if platform_user is None:
        return ''

    if 'id' not in platform_user or 'screen_name' not in platform_user:
        return ''

    pid = '{source}_{platform_uid}'.format(source=source, platform_uid=platform_user['id'])
    pid_uid_key = 'platform_uid:to:uid'

    conn = db.get_conn()
    uid = conn.hget(pid_uid_key, pid)
    if uid == None:
        uid = str(uuid.uuid1()).upper()
        conn.hset(pid_uid_key, pid, uid)

    user_key = 'user:{uid}'.format(uid=uid)

    pipe = conn.pipeline()

    # Save user data.
    pipe.hset(user_key, 'source', source)
    pipe.hset(user_key, 'platform_uid', platform_user['id'])
    pipe.hset(user_key, 'access_token', access_token)
    pipe.hset(user_key, 'name', platform_user['screen_name'])
    
    # Save token expires time.
    if expires_in.isdigit():
        token_score = int(time.time()) + int(expires_in)
        pipe.zadd('token_expires', token_score, user_key)

    pipe.execute()

    # Set cookies.
    resp = make_response()
    resp.set_cookie('uid', uid, max_age=864000)
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('uid', '', max_age=0)
    return resp

@app.route('/wb_callback')
def weibo_callback():
    return render_template('weibo_callback.html')


if __name__ == "__main__":
    #app.debug = True
    app.run()