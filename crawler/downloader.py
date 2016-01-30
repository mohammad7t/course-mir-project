from settings import CACHE_DIR

RESEARCHERS_CACHE_DIR = CACHE_DIR / 'researchers'
PUBLICATIONS_CACHE_DIR = CACHE_DIR / 'publications'


def download_and_get_links(resource):
    if resource.cache_path.exists():
        return resource.links_path.lines()


