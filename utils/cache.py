from django.core.cache import cache


class CacheInterface:
    def __init__(self, default_timeout=3600):
        self.cache = cache
        self.default_timeout = default_timeout

    def set(self, key, value, timeout=None):
        return self.cache.set(key, value, timeout or self.default_timeout)

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def delete(self, key):
        return self.cache.delete(key)


cache = CacheInterface()
