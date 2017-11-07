# File Settings
file_directory = '../data/ecmwf'
logging_directory = '../data/logs'
file_prefix = 'an-'
__file_suffix = '.grib'
# Multi-threading options
executor_thread_pool_size = 2
future_timeout=60*4 # 5 min timeout

# Time
date_format = '%Y-%m-%dT%H:%M:%S'

# Logging
log_format="[%(asctime)s] - %(levelname)s: %(message)s"