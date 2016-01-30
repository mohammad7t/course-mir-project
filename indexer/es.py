from os import walk
from pprint import pprint
import copy

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
            # body={
            #     'settings': {
            #         # just one shard, no replicas
            #         'number_of_shards': 1,
            #         'number_of_replicas': 0,
            #
            #         # custom analyzer for analyzing file paths
            #         'analysis': {
            #             'analyzer': {
            #                 'file_path': {
            #                     'type': 'custom',
            #                     'tokenizer': 'path_hierarchy',
            #                     'filter': ['lowercase']
            #                 }
            #             }
            #         }
            #     }
            # }
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

def _add_term_vector_to_tf_map(tf_map, term_vector):
    for term, props in term_vector.items():
        tf_map[term] = tf_map.get(term, 0) + props['term_freq']


def _add_term_vector_to_df_map(df_map, term_vector):
    for term, props in term_vector.items():
        df_map[term] = df_map.get(term, 0) + props['doc_freq']


def _add_publication_map_vector(id, tf_map, df_map):
    result = es.termvectors(
            index=ELASTIC_INDEX_NAME,
            doc_type='publication',
            id=id,
            fields='title,abstract',
            positions=False, offsets=False, term_statistics=True,
    )['term_vectors']
    _add_term_vector_to_df_map(df_map, result['abstract']['terms'])
    _add_term_vector_to_df_map(df_map, result['title']['terms'])
    _add_term_vector_to_tf_map(tf_map, result['abstract']['terms'])
    _add_term_vector_to_tf_map(tf_map, result['title']['terms'])
    return tf_map

def search(query):
    result= es.search(index=ELASTIC_INDEX_NAME, doc_type='publication', q=query)
    return [hit['_source'] for hit in result['hits']['hits']]


def get_publications_freq_maps():
    pubs = _get_all_publications()
    doc_tf_map = {}
    df_map = {}
    for pub in pubs:
        doc_id = pub['id']
        tf_map = {}
        _add_publication_map_vector(doc_id, df_map, tf_map)
        doc_tf_map[doc_id] = tf_map

    return doc_tf_map, df_map


def update_ranks(pubs, ranks):
    for pub, rank in zip(pubs, ranks):
        new_pub = copy.copy(pub)
        new_pub['rank'] = rank
        es.update(index=ELASTIC_INDEX_NAME, doc_type='publication', id=pub['id'], body=new_pub)
