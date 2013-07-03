# –*- encoding:utf8 –*-
site_name = u'爱妹抖'
site_domain = 'imeidou.com'
weibo_app_key = 907513447
ga_tracking_id = 'UA-40272531-2'

admin_uid = '0802701A-DB42-11E2-A438-6167C370CE32'

db_host = 'imeidou.com'
db_port = 6379
db_pwd = 'CL1IzaHi8b5Ns83B4rrX'

def getconfig():
    ret = globals()
    del ret['__builtins__']
    del ret['__name__']
    del ret['__doc__']
    return ret