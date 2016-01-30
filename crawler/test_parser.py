from crawler import parser
from crawler.factory import resource_from_url


def test_parse_url():
    result = parser.parse_url(
            'https://www.researchgate.net/publication/285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search')
    assert result == {
        'type': 'publication',
        'uid': '285458515',
    }

    result = parser.parse_url(
            'https://www.researchgate.net/researcher/8159937_Zoubin_Ghahramani')
    assert result == {
        'type': 'researcher',
        'uid': '8159937',
    }
