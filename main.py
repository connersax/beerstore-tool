import argparse
import string

import requests
from bs4 import BeautifulSoup

from beer import Beer

parser = argparse.ArgumentParser()
beerStoreUrl = "https://www.thebeerstore.ca/beers/"

headers = {
	'User-Agent': '',
	'Cookie': 'beer_home_store=3256',
}
# Dougall = 3256
# Lakefield = 4709

parser.add_argument("beer")

args = parser.parse_args()
beerArg = args.beer

reqData = requests.get(beerStoreUrl + beerArg, headers=headers)
status = reqData.status_code
soup = BeautifulSoup(reqData.content, 'html.parser')

beerName = string.capwords(soup.find("div", class_="desc").find(
	"h1", class_="capitalize").contents[0])

htmlBeerFormats = soup.findAll("div", class_="total_cans")
htmlAllBeer = []
allBeer = []

for beerType in htmlBeerFormats:
	for beer in beerType.findAll("li", class_="d-column d-row option _cart"):
		htmlAllBeer.append(beer)

for beer in htmlAllBeer:
	quanTypeStr = str(
		beer.find("div", class_="col_1 first col_same").contents[2]).strip()

	stock = 0
	if (len(beer.find("div", class_="col_2 second col_same").contents) == 3):
		stock = int(
			str(beer.find("div", class_="col_2 second col_same").contents[2]).strip())
	elif (beer.find("div", class_="col_2 second col_same").find("span", class_="outStock")):
		stock = 0
	else:
		stock = "Packup"

	salePrice = float(
		str(beer.find("span", class_="sale_price").contents[0]).strip()[1::])
	onSale = True if beer.find("span", class_="sale_badge") else False

	allBeer.append(Beer(beerName, quanTypeStr, salePrice, stock, onSale))

allBeer.sort(key=Beer.sortBy, reverse=True)

# for beer in allBeer:
#     print("""
# {}{}
# {} {} × {}ml at ${:.2f}
# {:.4f}ml/$
#     """.format(beerName, " (On Sale)" if beer.onSale else "", beer.quantity, beer.type, beer.serving, beer.price, beer.mlPerDollar))

bestOption: Beer
for beer in allBeer:
	if (beer.inStock):
		bestOption = beer
		break

try:
	bestOption
except NameError:
	print("There was no {} in stock, looks like you'll have to try another beer.".format(beerName))
else:
	print("""
{}{}
Best: {} {} \u00d7 {}ml at ${:.2f}
	  {:.4f}ml/$
	""".format(beerName, " (On Sale)" if bestOption.onSale else "", bestOption.quantity, bestOption.type, bestOption.serving, bestOption.price, bestOption.mlPerDollar))
