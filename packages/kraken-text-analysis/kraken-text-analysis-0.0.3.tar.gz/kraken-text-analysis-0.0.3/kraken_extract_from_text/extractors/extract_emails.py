
import re



def get(content):
    
    emails = get_emails(content)

    records = []

    for email in emails:
        records.append(get_contactpoint_record(email))
    
    return records


def get_emails(content):
    """
    """
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", content)

    return emails


def get_contactpoint_record(email):
    """
    """
    record = {

        '@type': 'schema:ContactPoint',
        'schema:email': email
    }
    return record

