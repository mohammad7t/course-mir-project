import logging
from pprint import pprint

import json
import requests
from bs4 import BeautifulSoup

from settings import CACHE_DIR

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0'

(CACHE_DIR / 'researcher').makedirs_p()
(CACHE_DIR / 'publication').makedirs_p()

def ajax_get(url):
    response = requests.get(url, headers={'User-Agent': USER_AGENT,
                                          'Accept': 'application/json, text/javascript, */*; q=0.01',
                                          'X-Requested-With': 'XMLHttpRequest'})
    if (response.status_code != 200):
        return {}
    return response.json()


def download_and_get_links(resource):
    from crawler.parser import parse_researcher, parse_publication

    if resource.links_path.exists():
        return resource.links_path.lines()

    response = requests.get(resource.url, headers={'User-Agent': USER_AGENT})
    if response.status_code != 200:
        logging.error('could not get url {}'.format(resource.url))
        return []
    soup = BeautifulSoup(response.text, 'html.parser')

    if resource.type == 'researcher':
        links, data = parse_researcher(resource, soup)
    else:
        links, data = parse_publication(resource, soup)
    resource.cache_path.write_text(json.dumps(data))
    resource.links_path.write_lines(links)
    return links
