

from kraken_extract_from_text import extractors

def get(content):
    """
    """


    results = []

    # Get emails
    results += extractors.extract_emails.get(content)

    # Get urls
    results += extractors.extract_urls.get(content)


    # Get ioc
    results += extractors.extract_ioc.get(content)
    
    return results