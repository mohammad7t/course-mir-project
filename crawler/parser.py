from pprint import pprint

import logging

from urllib.parse import urljoin

from crawler.downloader import ajax_get
from settings import CRAWLER_IN_DEGREE, CRAWLER_OUT_DEGREE


def parse_url(url: str):
    for type in ['researcher', 'publication']:
        pos = url.find('/{}/'.format(type))
        if pos > 0:
            return {'type': type, 'uid': url[pos + len(type) + 2:url.find('_', pos + 1)]}
    raise RuntimeError('Invalid url')


def parse_researcher(resource, soup):
    name = soup.select('.profile-header-name .fn,.ga-profile-header-name')[0].string
    print([resource.make_url(link['href']) for link in soup.select('.js-publication-title-link')])
    return [], {'id': resource.uid, 'name': name}


def parse_publication(resource, soup):
    logging.info('parsing ' + resource.url)
    from crawler.downloader import ajax_get
    title, abstract = '', ''
    links = []
    try:
        try:
            title = soup.select('h1.pub-title')[0].string
            abstract = soup.select('.pub-abstract div div')[0].getText()
        except IndexError:
            title = soup.select('.publication-title')[0].string
            abstract = soup.select('.publication-abstract-text')[0].getText()
    except Exception:
        logging.exception('could not parse page content {}'.format(resource.url))
        return [], {}

    authors = []
    AUTHORS_URL = 'https://www.researchgate.net/publicliterature.PublicationAuthorList.html?publicationUid={}'
    resp = ajax_get(AUTHORS_URL.format(resource.uid))
    for author in resp['result']['state']['publicationAuthors']['loadedItems']:
        links.append(urljoin('https://www.researchgate.net/', author['authorURL']))
        authors.append({'uid': author['authorUid'], 'name': author['nameOnPublication']})

    citations = []
    try:
        citation_link = 'https://www.researchgate.net/publicliterature.PublicationIncomingCitationsList.html?publicationUid=' + \
                        resource.uid + \
                        '&citedInPage=1&swapJournalAndAuthorPositions=0&showAbstract=1&showType=1&showPublicationPreview=1'
        resp = ajax_get(citation_link)
        citations = [c['data']['publicationUid'] for c in resp['result']['data']['citationItems']]
        links.extend([c['data']['publicationUrl'] for c in resp['result']['data']['citationItems']][:CRAWLER_IN_DEGREE])
    except Exception:
        pass

    references = []
    try:
        reference_link = 'https://www.researchgate.net/publicliterature.PublicationCitationsList.html?publicationUid=' + \
                         str(resource.uid) + \
                         '&showCitationsSorter=true&showAbstract=true&showType=true&showPublicationPreview=true&swapJournalAndAuthorPositions=false'
        resp = ajax_get(reference_link)
        references = [r['data']['publicationUid'] for r in resp['result']['data']['citationItems']]
        links.extend([r['data']['publicationUrl'] for r in resp['result']['data']['citationItems']][:CRAWLER_OUT_DEGREE])
    except Exception:
        pass

    links = [urljoin('https://www.researchgate.net/', link) for link in links]

    return links, {
        'title': title, 'id': resource.uid, 'abstract': abstract, 'citations': citations,
        'references': references, 'authors': authors
    }
