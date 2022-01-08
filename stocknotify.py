# stocknotify.py
# Kelby Hubbard
# Started: 2022-01-06
# Updated: 2022-01-07

# Notify a user on Discord of potential PS5 in stock using Discord webhook and html parsing. Currently works with Bestbuy & Playstation direct.

import requests
from bs4 import BeautifulSoup
import time


userID = ""
webhookURL = ""

def grab_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content

def check_item_in_stock(page_html, site):
    soup = BeautifulSoup(page_html, 'html.parser')

    if (site == "bestbuy"):
        out_of_stock_divs = soup.findAll("button", {"data-button-state": "SOLD_OUT"})

    # FIXME: False positives occasionally.
    if (site == "amazon"):
        out_of_stock_divs = soup.findAll("div", {"id":"outOfStock"})

    # FIXME: Doesn't work.
    if (site == "walmart"):
        out_of_stock_divs = soup.findAll("div", {"data-testid":"buy-box-ad"})

    if (site == "playstation"):
        out_of_stock_divs = soup.findAll("link", {"href":"https://schema.org/OutOfStock"})
        
    return len(out_of_stock_divs) == 0

def check(url, site):
    page_html = grab_html(url)

    # In stock
    if check_item_in_stock(page_html, site):
        in_stock = "<@!" + userID + "> this is in stock now! [Link here](" + url + ")"
        msg = {"content": in_stock}
        requests.post(webhookURL, data=msg)
    
    # Out of stock
    else:
        oos = site + " out of stock."
        print(oos)


def main():
    bestbuyPS5Disk = "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"
    bestbuyPS5Digital = "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161"
    playstationDigital = "https://direct.playstation.com/en-us/consoles/console/playstation5-digital-edition-console.3006647"
    playstationDisk = "https://direct.playstation.com/en-us/consoles/console/playstation5-console.3006646"
 
    while True:
        check(bestbuyPS5Disk, "bestbuy")
        time.sleep(15)
        check(bestbuyPS5Digital, "bestbuy")
        time.sleep(15)
        check(playstationDigital, "playstation")
        time.sleep(15)
        check(playstationDisk, "playstation")
        time.sleep(15)

main()



# amazonPS5Console = "https://www.amazon.com/PlayStation-5-Console/dp/B09DFCB66S"
# walmartPS5Disk = "https://www.walmart.com/ip/PlayStation-5-Console/363472942?irgwc=1&sourceid=imp_QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&veh=aff&wmlspartner=imp_1943169&clickid=QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383"
# walmartPS5Digital = "https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815?irgwc=1&sourceid=imp_QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&veh=aff&wmlspartner=imp_1943169&clickid=QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383"