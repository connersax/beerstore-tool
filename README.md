# The Beer Store Price Tool

A tool designed to help a user find the cheapest way to buy a case of beer. The tool works by first asking the user to search for their preferred store. The user is then asked to search for a beer they are planning to buy. The tool will then output the cheapest price per milliliter case for that beer in stock at that store.

Information is scraped from [The Beer Store's](https://www.thebeerstore.ca/) website.

## Dependencies

- Python 3.10 (tested)

## Running

Steps will be based off creation of Python virtual environment. In this directory follow these steps:

1. Create and activate virtual environment, I named mine `beer_env`
2. Install Python dependencies using: `pip install -r requirements.txt`
3. Now `main.py` will be runnable

### Regenerating JSON files

In the case of a new store or beer that isn't in the options after searching a user can follow these steps to regenerate the JSON files. Do not constantly run these. You may be flagged and blocked by The Beer Store's servers. Considering you're using this tool I think you'll want to continue to view their website.

1. Ensure you are in the virtual environment and in the `/generators` directory
2. For `stores_ids.json` run `stores_to_json.py`
3. For `beer_ids.json`
   1. Go to the [Beers](https://www.thebeerstore.ca/beers/) site and load all the beers by scrolling until you have reached the bottom of the page.
   2. Right click and save the HTML file as `beer.html`, make sure you have the `Webpage, Complete` option selected when saving so the loaded beers are saved in the HTML file.
   3. Place the `beer.html` file in the current `/generators` directory
   4. Run `beer_to_json.py`

## For the Future
- [ ] Fix the `beer_to_json.py` so it's fully automatic and doesn't require the user to download the HTML file manually.
- [ ] Add an argument when running `main.py` so user can generate new JSONs directly from the main tool. This will make the tool more complete.