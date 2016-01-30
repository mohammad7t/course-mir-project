import json

from indexer import es
from settings import CACHE_DIR


def rebuild():
    es.reset_whole_index()
    files = list((CACHE_DIR / 'publication').walkfiles('*.json'))
    i = 0
    for file in files:
        i+=1
        publication = json.loads(file.text())
        (CACHE_DIR/'indexer.progress').write_text('%d / %d' % (i, len(files)))
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


if __name__ == '__main__':
    rebuild()
