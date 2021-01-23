
# Additional info: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python

from bs4 import BeautifulSoup as bs
import requests
import argparse
from tqdm import tqdm
import datetime
import logging

from re import sub


parser = argparse.ArgumentParser()

parser.add_argument("--verbose", "-v", help="True to enable verbose logging to console", type=bool, required=False, default=True)
parser.add_argument("--maxPages", "-m", help="Max # of pages to scrape (default 40)", type=int, required=False, default=40)
parser.add_argument("--zumperURL", "-z",
                    help="Pass a zumper url of the form `https://www.zumper.com/apartments-for-rent/san-francisco-ca/2-beds?bathrooms=2`",
                    type=str,
                    required=False,
                    default="https://www.zumper.com/apartments-for-rent/san-francisco-ca/mission-dolores/2-beds?bathrooms=2&box=-122.47472544836458,37.72517967784283,-122.38697729132755,37.80021764760265")  # Bounding box is the desired area on the map

args = parser.parse_args()

max_pages = args.maxPages
urls = ["{}&page={}"
        .format(args.zumperURL, i) for i in range(1, max_pages)]


def priceFromListItem(item):
    return int(sub(r"\D", "", str(item.contents)))

def fetchPrices():
    all_prices = []
    for url in tqdm(urls):
        r = requests.get(url)
        if r.status_code == 404:
            print("Invalid page, ending!")
            break
        soup = bs(r.content, 'html.parser')
        info_panes = soup.findAll('div', class_="ListItemMobileView_price__1IH5H")
        info_panes = map(priceFromListItem, info_panes)
        all_prices.extend(info_panes)



    sum_price = float(sum(all_prices))
    avg_price = sum_price / len(all_prices)
    print("Found {} prices".format(len(all_prices)))
    print("The average price was ${:.2f}".format(avg_price))

    logging.basicConfig(filename="PriceLog.txt",
                        level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S')

    logging.info("Num Listings Scraped: {}, Avg Price: {:.2f}. Src: {}".format(
        len(all_prices), avg_price, args.zumperURL
    ))

if __name__ == "__main__":
    fetchPrices()