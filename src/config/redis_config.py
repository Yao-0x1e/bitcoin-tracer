import redis

from src.config.app_config import app_ini as ai

redis_pool = redis.ConnectionPool(
    host=ai.get('redis', 'host'),
    port=ai.getint('redis', 'port'),
    password=ai.get('redis', 'password'),
    db=ai.getint('redis', 'db')
)
redis_conn = redis.Redis(connection_pool=redis_pool)
