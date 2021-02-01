import http3
from bs4 import BeautifulSoup

client = http3.AsyncClient()


async def call_api(url: str):
    r = await client.get(url)
    return r


async def ebay_api(search_keyword, url: str = ''):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={search_keyword}&_sacat=0'
    response = await call_api(url)
    ebay_soup = BeautifulSoup(response.text, 'html.parser')
    return ebay_soup.find_all('li', {'class': 's-item'})


async def amazon_api(search_keyword, url: str = ''):
    url = ''
    response = await call_api(url)

    return response


async def aliexpress_api(search_keyword, url: str = ''):
    url = ''
    response = await call_api(url)

    return response


async def shopify_api():
    url = ''

    response = await call_api(url)

    return response