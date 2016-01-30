import logging

from crawler.parser import parse_url
from crawler.resource import Resource


def resource_from_url(url):
    try:
        parsed = parse_url(url)
    except RuntimeError:
        logging.exception('could not parse url')
    return Resource(type_=parsed['type'], url=url, uid=parsed['uid'])
