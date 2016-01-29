import logging

from crawler.parser import parse_url
from settings import CACHE_DIR


class Resource:
    def __init__(self, url):
        self.url = url
        try:
            parsed = parse_url(url)
            self.is_invalid = False
        except RuntimeError:
            logging.exception('could not parse url')
            self.is_invalid = True
        self.type = parsed['type']
        self.uid = parsed['uid']

    @property
    def cache_path(self):
        return CACHE_DIR / self.type / self.uid + '.json'

