from ioc_finder import find_iocs



def get(content):

    iocs = find_iocs(content)


    for key, value in iocs.items():
        print(key, value)
    

    records = []
    
    # Get domains
    for i in iocs.get('domains', []):
        record = {
            '@type': 'schema:WebSite',
            'schema:url': 'https://' + str(i)
        }
        records.append(record)

    # Get urls
    for i in iocs.get('urls', []):
        record = {
            '@type': 'schema:WebPage',
            'schema:url': i
        }
        records.append(record)


    # Get emails
    for i in iocs.get('email_addresses', []):
        record = {
            '@type': 'schema:contactPoint',
            'schema:email': i
        }
        records.append(record)

        
    return records

