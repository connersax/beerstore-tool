import json

import requests
from bs4 import BeautifulSoup

from beer import Beer


if __name__ == '__main__':
    beerstore_url = 'https://www.thebeerstore.ca/beers/'
    json_stores: dict
    json_beers: dict
    out_msg: str

    # Search and select store
    with open('json/store_ids.json', 'r') as infile:
        json_stores = json.load(infile)

    selected_store = input('Search for preferred store: ')
    searched_stores = dict()
    
    counter = 1
    for store in json_stores.values():
        if selected_store.lower() in store[0].lower() or selected_store.lower() in store[1].lower():
            searched_stores.update({counter: store})
            print(f'{counter}. {store[1]}')
            counter += 1

    selected_store = input('Select a store by number: ')
    selected_store = searched_stores.get(int(selected_store))[2]

    print(f'Store {json_stores.get(str(selected_store))[0]}, at {json_stores.get(str(selected_store))[1]} selected!\n')
    ##############################################################
    
    # Search and select beer
    with open('json/beer_ids.json', 'r') as infile:
        json_beers = json.load(infile)

    selected_beer = input('Search for a beer: ')
    searched_beers = dict()

    counter = 1
    for beer in json_beers.values():
        if selected_beer.lower() in beer.get('name').lower() or selected_beer.lower() in beer.get('company').lower():
            searched_beers.update({counter: beer})
            print(f'{counter}. {beer.get("name")}')
            counter += 1

    selected_beer = input('Select a beer by number: ')
    selected_beer = searched_beers.get(int(selected_beer)).get('link')

    print(f'Beer {json_beers.get(selected_beer).get("name")} selected!\n')
    ##############################################################

    headers = {
        'User-Agent': '',
        'Cookie': f'beer_home_store={selected_store}',
    }


    request = requests.get(beerstore_url + selected_beer, headers=headers)
    status = request.status_code
    soup = BeautifulSoup(request.content, 'html.parser')

    beer_name = soup.find('div', class_='desc').find('h1', class_='capitalize').contents[0]

    html_beer_formats = soup.findAll('div', class_='total_cans')
    html_all_beer = []
    all_beer = []

    for beer_type in html_beer_formats:
        for beer in beer_type.findAll('li', class_='d-column d-row option _cart'):
            html_all_beer.append(beer)

    for beer in html_all_beer:
        str_quan_type = str(beer.find('div', class_='col_1 first col_same').contents[2]).strip().split(" ")
        quantity = int(str_quan_type[0])
        type = str_quan_type[2]
        serving = str_quan_type[3]

        stock = 0
        if (len(beer.find('div', class_='col_2 second col_same').contents) == 3):
            stock = int(str(beer.find('div', class_='col_2 second col_same').contents[2]).strip())
        elif (beer.find('div', class_='col_2 second col_same').find('span', class_='outStock')):
            stock = 0
        else:
            stock = 'Packup'

        sale_price = float(str(beer.find('span', class_='sale_price').contents[0]).strip()[1::])
        on_sale = True if beer.find('span', class_='sale_badge') else False

        all_beer.append(Beer(beer_name, quantity, type, serving, sale_price, stock, on_sale))

    all_beer.sort(reverse=True)

    # for beer in all_beer:
    #     print(f'\n{beer}')

    bestOption: Beer
    beer: Beer
    for beer in all_beer:
        if (beer.inStock()):
            bestOption = beer
            break

    try:
        bestOption
    except NameError:
        out_msg = f'There was no {beer_name} in stock, looks like you\'ll have to try another beer.'
    else:
        out_msg = (
            'Best Option:\n'
            f'{bestOption}'
        )

    print(out_msg)
