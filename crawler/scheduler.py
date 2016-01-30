import queue

import logging

import json

from path import Path

from crawler.downloader import download_and_get_links
from crawler.factory import resource_from_url

from crawler.resource import Resource
from settings import CRAWLER_INITIAL_URLS, CACHE_DIR, CRAWLER_LIMIT_PUBLICATIONS, CRAWLER_LIMIT_RESEARCHERS


class Scheduler:
    def __init__(self):
        self.seen = set()
        self.q = queue.Queue()

    def visit(self, url_or_resource):
        if isinstance(url_or_resource, Resource):
            resource = url_or_resource
        else:
            resource = resource_from_url(url_or_resource)
        logging.info('visiting {}'.format(resource.url))
        if resource is None or self.is_seen(resource):
            return
        self.enqueue(resource)

    def is_seen(self, resource):
        return resource in self.seen

    def enqueue(self, resource):
        self.seen.add(resource)
        self.q.put(resource)

    def dequeue(self):
        return self.q.get()

    def limits_reached(self):
        def count_files(dir: Path):
            return len(list(dir.walkfiles('*.json')))

        pubs = count_files(CACHE_DIR / 'publication')
        auths = count_files(CACHE_DIR / 'researcher')
        status = {
            'publications': [pubs, CRAWLER_LIMIT_PUBLICATIONS],
            'researchers': [auths, CRAWLER_LIMIT_RESEARCHERS],
        }
        (CACHE_DIR / 'crawler.progress').write_text(json.dumps(status))
        return pubs >= CRAWLER_LIMIT_PUBLICATIONS and auths >= CRAWLER_LIMIT_RESEARCHERS

    def start(self):
        for url in CRAWLER_INITIAL_URLS:
            self.enqueue(resource_from_url(url))
        while (not self.q.empty() and not self.limits_reached()):
            resource = self.dequeue()
            for link in download_and_get_links(resource):
                self.visit(link)


if __name__ == '__main__':
    Scheduler().start()
