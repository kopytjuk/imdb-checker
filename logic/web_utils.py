from urllib3.util.retry import Retry

import requests
from requests.adapters import HTTPAdapter

def retry_session(retries, session=None, backoff_factor=0.3):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        method_whitelist=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session