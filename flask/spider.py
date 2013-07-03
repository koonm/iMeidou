# –*- encoding:utf8 –*-
import db
import config

target_uid = 1162709062
url = 'https://api.weibo.com/2/statuses/user_timeline.json?feature=1&{target_uid}' \
        .format(target_uid=target_uid)

def fetch(access_token):
    if access_token is None:
        return



if __name__ == "__main__":
    user_key = ''

    if config.admin_uid:
        user_key = 'user:{uid}'.format(uid=config.admin_uid)

    fetch()