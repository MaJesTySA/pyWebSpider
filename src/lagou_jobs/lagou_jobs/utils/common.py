import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    md5_url = hashlib.md5()
    md5_url.update(url)
    return md5_url.hexdigest()
