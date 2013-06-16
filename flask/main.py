from flask import Flask, url_for, redirect, render_template, request, make_response, session
import uuid
import config
import db

app = Flask(__name__)

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

    pid = '{source}_{platform_uid}'.format(source=source, platform_uid=platform_uid)
    pid_uid_key = 'platform_uid:{pid}:uid'.format(pid=pid)

    conn = db.get_conn()
    uid = conn.get(pid_uid_key)
    if uid == None:
        uid = str(uuid.uuid1()).upper()
        conn.set(pid_uid_key, uid)

    user_key = 'user:{uid}'.format(uid=uid)
    conn.hset(user_key, 'source', source)
    conn.hset(user_key, 'platform_uid', platform_uid)
    conn.hset(user_key, 'access_token', request.form['access_token'])

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