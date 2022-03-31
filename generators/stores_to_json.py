import asyncio
import json
import re

import aiohttp
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': ''}


async def main(debug=False):
    stores_URL = 'https://www.thebeerstore.ca/stores/'

    req = requests.get(stores_URL, headers=headers)

    soup = BeautifulSoup(req.content, 'html.parser')

    stores_html = soup.find_all('div', class_='new_store_box')
    store_URLs = list()
    delay = 0.25  # Delay between each request since I don't want to DDOS the Beer Store

    for store_html in stores_html:
        store_URLs.append(store_html.find('a', class_='site_default_btn', href=True)['href'])

    tasks = list()

    for url in store_URLs:
        tasks.append(asyncio.ensure_future(get_store_data(url, debug=debug)))
        await asyncio.sleep(delay)

    results = await asyncio.gather(*tasks)
    return results


async def get_store_data(url: str, debug=False):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            store_data = [url, resp.status]

            if(resp.status == 200):
                content = await resp.read()
                soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

                store_name = soup.find('div', class_='top_sectionDiv').find('h2').text.strip()
                store_address = soup.find('div', class_='address_sec').find('a').text.strip()
                store_id = soup.find('div', class_='top_sectionDiv').find('p').text.strip()
                store_id = int(re.search('[0-9]+', store_id).group())

                store_data.append(store_name)
                store_data.append(store_address)
                store_data.append(store_id)

            if(debug == True):
                print(f'GET html with RESPONSE: {resp.status} for {url}')
            return store_data


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(debug=True))

    dict_stores = dict()

    for res in results:
        url = res[0]
        status = res[1]

        if(status == 200):
            city = res[2]
            address = res[3]
            store_id = res[4]

            dict_stores.update({store_id: [city, address, store_id]})

        else:
            print(f'GET return code {status}, for site {url}')

    json_stores = json.dumps(dict_stores, indent=4)

    with open('../json/store_ids.json', 'w') as outfile:
        outfile.write(json_stores)
