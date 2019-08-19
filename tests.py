import requests
import bs4


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html')
    table = soup.find("table", id='proxylisttable')
    proxies = set()
    rows = table.findAll('tr')
    for row in rows:
        out = extract_ip(row)
        if out is not None:
            proxies.add(out)
    return proxies


def extract_ip(row):
    tds = row.findAll('td')
    if len(tds) > 0:
        return tds[0].string
    return None


def cycle_proxies()