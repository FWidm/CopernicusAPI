from concurrent.futures import ThreadPoolExecutor

from copernicus_api.misc import settings

executor = ThreadPoolExecutor(settings.executor_thread_pool_size)
