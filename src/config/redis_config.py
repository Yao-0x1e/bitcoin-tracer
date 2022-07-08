import redis
import ujson

from src.config.app_config import app_ini as ai

redis_pool = redis.ConnectionPool(
    host=ai.get('redis', 'host'),
    port=ai.getint('redis', 'port'),
    password=ai.get('redis', 'password'),
    db=ai.getint('redis', 'db')
)
redis_conn = redis.Redis(connection_pool=redis_pool)


def cacheable(prefix: str, separator: str = '_', ex: int = None, serializer=ujson.dumps, deserializer=ujson.loads, key_handler=None):
    def decorator(target):
        def wrapper(*args, **kwargs):
            # 一个星号将参数以元组的形式导入
            # 两个星号将参数以字典的形式导入
            params = [str(arg) for arg in args] + [str(kwarg) for kwarg in kwargs.values()]
            redis_key = f'{prefix}:{separator.join(params)}'.replace(' ', '')
            if key_handler is not None:
                redis_key = key_handler(redis_key)
            redis_val = redis_conn.get(redis_key)
            if redis_val is not None:
                return deserializer(redis_val)
            else:
                result = target(*args, **kwargs)
                redis_val = serializer(result)
                redis_conn.set(redis_key, redis_val, ex=ex)
                return result

        return wrapper

    return decorator


def cacheevit(prefix: str, separator: str = '_'):
    def decorator(target):
        def wrapper(*args, **kwargs):
            params = [str(arg) for arg in args] + [str(kwarg) for kwarg in kwargs.values()]
            redis_key = f'{prefix}:{separator.join(params)}'.replace(' ', '')
            result = target(*args, **kwargs)
            redis_conn.delete(redis_key)
            return result

        return wrapper

    return decorator
