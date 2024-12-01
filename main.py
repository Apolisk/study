from hashlib import blake2b

url_mapping = {}
base_url = "https://"

def expand_url(long_url: str) -> str:
    short_url = f"{base_url}{blake2b(long_url.encode(), digest_size=6).hexdigest()}"
    url_mapping[short_url] = long_url
    return short_url

def decrease_url(short_url: str) -> str:
    return url_mapping.get(short_url, "Такой URL не сокрашали")

long_url = "https://www.google.com"
shortened = expand_url(long_url)
print("Short:", shortened)

expanded = decrease_url(shortened)
print("Orig:", expanded)
