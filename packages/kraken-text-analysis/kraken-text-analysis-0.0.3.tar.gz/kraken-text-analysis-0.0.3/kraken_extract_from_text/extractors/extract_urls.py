
import url_finder


def get(content):
    
    urls = get_urls(content)

    records = []

    for url in urls:
        records.append(get_webpage_record(url))
    
    return records


def get_urls(content):
    """
    """
    urls = url_finder.get_urls(content)
    return urls


def get_webpage_record(url):
    """
    """
    record = {

        '@type': 'schema:WebPage',
        'schema:url': url
    }
    return record