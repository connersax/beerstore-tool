import pickle

import requests
from bs4 import BeautifulSoup

from beer import Beer
from beerid import beerid
from storeid import storeid


if __name__ == '__main__':
    beerstore_url = 'https://www.thebeerstore.ca/beers/'
    stores = list()
    beers = list()
    out_msg: str

    # Search and select store
    with open('data/store_ids.pkl', 'rb') as infile:
        stores = pickle.load(infile)

    search_store_str = input('Search for preferred store: ')
    searched_stores = dict()
    
    counter = 1
    store: storeid
    for store in stores:
        if search_store_str.lower() in store.name.lower() or search_store_str.lower() in store.address.lower():
            searched_stores.update({counter: store})
            print(f'{counter}. {store.address}')
            counter += 1

    selected_store_index = int(input('Select a store by number: '))
    selected_store: storeid = searched_stores.get(selected_store_index)

    print(f'Store {selected_store.name}, at {selected_store.address} selected!\n')
    ##############################################################
    
    # Search and select beer
    with open('data/beer_ids.pkl', 'rb') as infile:
        beers = pickle.load(infile)

    searched_beer_str = input('Search for a beer: ')
    searched_beers = dict()

    counter = 1
    beerval: beerid
    for beerval in beers:
        if searched_beer_str.lower() in beerval.name.lower() or searched_beer_str.lower() in beerval.brewer.lower():
            searched_beers.update({counter: beerval})
            print(f'{counter}. {beerval.name}')
            counter += 1

    searched_beers_index = int(input('Select a beer by number: '))
    print(searched_beers_index)
    selected_beer: beerid = searched_beers.get(searched_beers_index)

    print(f'Beer {selected_beer.name} selected!\n')
    ##############################################################

    headers = {
        'User-Agent': '',
        'Cookie': f'beer_home_store={selected_store.id}',
    }


    request = requests.get(beerstore_url + selected_beer.link, headers=headers)
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
