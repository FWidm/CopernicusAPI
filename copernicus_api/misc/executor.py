from concurrent.futures import ThreadPoolExecutor

from copernicus_api.misc import settings

executor = ThreadPoolExecutor(settings.executor_threadpool_size)
