import logging

from settings import CACHE_DIR

logging.basicConfig(filename=CACHE_DIR/'log.txt', level=logging.INFO)
