import redis
import json

class redisWorker:
    def __init__(
            self, 
            host: str = 'localhost', 
            port: int = 6379, 
            expire: int = 3600,
            active = True
        ) -> None:

        self.active = active
        self.expire = expire
        self.client = redis.Redis(host=host, port=port) if active else None

    def cache(self, key, callable, *args, **kwargs):
        if not self.active:
            return callable(*args, **kwargs)

        value = self.client.get(key)

        if value == None:
            value = callable(*args, **kwargs)
            self.client.set(key, json.dumps(value), ex=self.expire)
        else:
            value = json.loads(value)

        return value
    
    def flushall(self):
        self.client.flushall()