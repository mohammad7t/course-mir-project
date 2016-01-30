import json

from indexer import es
from settings import CACHE_DIR


def rebuild():
    es.reset_whole_index()
    for file in (CACHE_DIR / 'publication').walkfiles('*.json'):
        publication = json.loads(file.text())
        if not publication:
            continue
        es.index_publication(
                id=publication['id'],
                title=publication['title'],
                abstract=publication['abstract'],
                authors=publication['authors'],
                cited_ids=publication['citations'],
                reference_ids=publication['references'],
        )
    es.refresh()

rebuild()
