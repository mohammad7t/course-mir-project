from settings import CACHE_DIR


class Resource:
    def __init__(self, url, type_, uid):
        self.url = url
        self.type = type_
        self.uid = uid

    @property
    def cache_path(self):
        return CACHE_DIR / self.type / (self.uid + '.json')

    @property
    def links_path(self):
        return CACHE_DIR / self.type / (self.uid + '.links')

    def __hash__(self):
        return hash((self.type, self.uid))

    def __eq__(self, other):
        return (self.type, self.uid) == (other.type, other.uid)
