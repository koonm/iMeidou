import redis
import config

pool = redis.ConnectionPool(host=config.db_host, port=config.db_port, password=config.db_pwd, db=0, decode_responses=True)

def get_conn():
    conn = redis.StrictRedis(connection_pool=pool)
    return conn