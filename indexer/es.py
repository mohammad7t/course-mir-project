from os import walk
from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from settings import ELASTIC_INDEX_NAME

es = Elasticsearch()


def index_publication(id, title, abstract, cited_ids, reference_ids, authors):
    body = dict(id=id, title=title, abstract=abstract, authors=authors, cited_ids=cited_ids,
                reference_ids=reference_ids)
    es.index(index=ELASTIC_INDEX_NAME, doc_type='publication', body=body, id=id)


def reset_whole_index():
    try:
        es.indices.delete(index=ELASTIC_INDEX_NAME)
    except NotFoundError:
        pass
    es.indices.create(
            index=ELASTIC_INDEX_NAME,
    )


def refresh():
    es.indices.refresh(index=ELASTIC_INDEX_NAME)


def _get_all_publications():
    result = es.search(index=ELASTIC_INDEX_NAME, doc_type='publication', body={'query': {'match_all': {}}},
                       scroll='10s', size=1000)
    ret = []
    scroll_id = result['_scroll_id']
    while len(result['hits']['hits']) > 0:
        ret += [hit['_source'] for hit in result['hits']['hits']]
        result = es.scroll(scroll_id=scroll_id, scroll='10s')
    es.clear_scroll(scroll_id=scroll_id)
    return ret


def _add_term_vector_to_map_vector(map_vector, term_vector):
    for term, props in term_vector.items():
        map_vector[term] = map_vector.get(term, 0) + props['term_freq']


def _get_publication_map_vector(id):
    map_vector = {}
    result = es.termvectors(
            index=ELASTIC_INDEX_NAME,
            doc_type='publication',
            id=id,
            fields='title,abstract',
            positions=False, offsets=False, term_statistics=True,
    )['term_vectors']
    _add_term_vector_to_map_vector(map_vector, result['abstract']['terms'])
    _add_term_vector_to_map_vector(map_vector, result['title']['terms'])
    return map_vector


def get_publications_tf_map():
    pubs = _get_all_publications()
    return {pub['id']: _get_publication_map_vector(pub['id']) for pub in pubs}

print(get_publications_tf_map())
