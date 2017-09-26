from werkzeug.contrib.cache import SimpleCache
timeout = 60 * 60 # 1h cache
retrieve_timeout = 60 * 60 * 24 # 24h cache

#todo: swap out in production!
cache = SimpleCache()
