import json

from indexer import es
from settings import CACHE_DIR


def rebuild():
    es.reset_whole_index()
    for file in (CACHE_DIR / 'publication').walkfiles('*.json'):
        publication = json.loads(file.text())
        es.index_publication(
                id=publication['id'],
                title=publication['name'],
                abstract=publication['abstraction'],
                authors=[],
                cited_ids=publication['citedInIDs'],
                reference_ids=publication['refrenceIDs'],
        )
    es.refresh()


rebuild()
