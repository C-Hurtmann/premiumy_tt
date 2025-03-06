from pathlib import Path
import random
import requests


with open(Path('proxyscrape_premium_http_proxies.txt')) as f:
    proxy = random.choice(f.readlines())


res = requests.get('https://2ip.me/en/', proxies={'http': proxy, 'https': proxy})

print(res.text)
