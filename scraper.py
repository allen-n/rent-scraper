
# Additional info: https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python

from bs4 import BeautifulSoup as bs
import requests
import argparse
from tqdm import tqdm
import datetime
import logging
import statistics
from random import randint

from re import sub


parser = argparse.ArgumentParser()

parser.add_argument("--verbose", "-v", help="Enable verbose logging to console", action='store_true',
                    required=False, default=True)
parser.add_argument("--proxy", "-p", help="Use random proxies for each scraping call. MUCH Slower but obfuscates IP Address. Also foregoes HTTPS since not all proxies support it.", action='store_true',
                    required=False, default=False)
parser.add_argument("--maxPages", "-m", help="Max # of pages to scrape (default 100)",
                    type=int, required=False, default=100)
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


def getProxyIPs():
    r = requests.get("https://www.us-proxy.org/")
    soup = bs(r.content, 'html.parser')
    table = soup.find('table', attrs={"id": "proxylisttable"})
    rows = table.findAll('tr')
    proxies = []
    for row in rows:
        ip = row.findNext('td')
        port = ip.findNext('td')

        proxy = u"{}:{}".format(ip.contents[0], port.contents[0])
        proxies.append(proxy)
    proxies.pop()
    return proxies


def fetchPrices():
    all_prices = []
    for url in tqdm(urls):
        r = None
        if args.proxy:
            proxies = getProxyIPs()
            i = randint(0, len(proxies)-1)
            r = requests.get(url, proxies={
                "http": proxies[i]
            })
        else:
            r = requests.get(url)
        if r.status_code == 404:
            print("Invalid page, ending!")
            break
        soup = bs(r.content, 'html.parser')
        info_panes = soup.findAll(
            'div', class_="ListItemMobileView_price__1IH5H")
        if(len(info_panes) == 0):
            print("No more results, ending!")
            break
        info_panes = map(priceFromListItem, info_panes)
        all_prices.extend(info_panes)

    # sum_price = float(sum(all_prices))
    if all_prices:
        avg_price = statistics.mean(all_prices)  # sum_price / len(all_prices)
        std_dev = statistics.stdev(all_prices)
        mode = None
        median = None
        try:
            mode = statistics.mode(all_prices)
            median = statistics.median(all_prices)
        except statistics.StatisticsError:
            mode = avg_price
            print("No mode!")
        print("Found {} prices".format(len(all_prices)))
        print("The average price was ${:.2f}".format(avg_price))

        logging.basicConfig(filename="PriceLog.txt",
                            level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S')

        logging.info("Num Listings Scraped: {}, Avg Price: {:.2f}, StdDev Price: {:.2f}, Median Price: {:.2f}, Mode Price: {:.2f}. Src: {}".format(
            len(all_prices), avg_price, std_dev, median, mode, args.zumperURL
        ))


if __name__ == "__main__":
    fetchPrices()
