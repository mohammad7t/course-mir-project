from path import Path

PROJECT_ROOT = Path(__file__).dirname()

ELASTIC_INDEX_NAME = 'mir'

CACHE_DIR = PROJECT_ROOT / 'cache'
CRAWLER_INITIAL_URLS = [
    'https://www.researchgate.net/researcher/8159937_Zoubin_Ghahramani',
]
