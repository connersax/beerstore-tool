import json
import re

from bs4 import BeautifulSoup

headers = {'User-Agent': ''}


def main():
    beers_html: str
    dict_beers = dict()

    with open('beer.html', 'r') as infile:
        beers_html = infile.read()

    soup = BeautifulSoup(beers_html, 'html.parser')
    soup = soup.find_all('div', class_='result_box')

    for beer in soup:
        dict_beer = dict()
        name = beer.find('span').text
        name = re.sub('\s+', ' ', name).__str__()
        company = beer.find('p').text
        link = beer.find('a')['href'][7:-1]

        dict_beer.update({'name': name})
        dict_beer.update({'company': company})
        dict_beer.update({'link': link})

        dict_beers.update({link: dict_beer})

    json_beers = json.dumps(dict_beers, indent=4)

    with open('../json/beer_ids.json', 'w') as outfile:
        outfile.write(json_beers)


if __name__ == '__main__':
    main()
