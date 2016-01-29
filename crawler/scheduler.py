import queue

from crawler import parser

from crawler.resource import Resource
from settings import CACHE_DIR
from collections import defaultdict


class Scheduler:
    def __init__(self):
        self.q_set = defaultdict(set)
        self.q = queue.Queue()

    def schedule(self, url):
        resource = Resource(url)
        if resource.is_invalid or self.is_seen(resource):
            return
        self.enqueue(resource)

    def is_seen(self, resource):
        return (resource.uid in self.q_set[resource.type]) or resource.cache_path.exists()

    def enqueue(self,resource):
        self.q_set[resource.type].add(resource.uid)
        self.q.put(resource)

    def dequeue(self):
        resource = self.q.get()
        self.q_set[resource.type].remove(resource.uid)
