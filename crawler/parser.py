def parse_url(url: str):
    for type in ['researcher', 'publication']:
        pos = url.find('/{}/'.format(type))
        if pos > 0:
            return {'type': type, 'uid': url[pos + len(type) + 2:url.find('_', pos + 1)]}
    raise RuntimeError('Invalid url')
