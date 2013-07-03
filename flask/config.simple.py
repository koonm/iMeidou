# –*- encoding:utf8 –*-
site_name = u'爱妹抖'
site_domain = 'imeidou.com'
weibo_app_key = 1234567890
ga_tracking_id = 'UA-40272531-2'

db_host = 'localhost'
db_port = 6379
db_pwd = 'password'

def getconfig():
    ret = globals()
    del ret['__builtins__']
    del ret['__name__']
    del ret['__doc__']
    return ret