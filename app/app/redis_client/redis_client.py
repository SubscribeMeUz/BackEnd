import redis


redis_storage = redis.Redis(host='localhost', port=6379, db=5, protocol=2)



