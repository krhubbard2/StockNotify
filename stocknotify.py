# stocknotify.py
# Kelby Hubbard
# Started: 2022-01-06
# Updated: 2022-01-09

# Notify a user via Discord, email, or sms text of potential PS5 in stock using Discord webhook, html parsing and smtplib. Currently works with Bestbuy & Playstation direct.

import requests
from bs4 import BeautifulSoup
import time
import smtplib, ssl # For email notification
from email.mime.text import MIMEText # For txt notifcation
from email.mime.multipart import MIMEMultipart

port = 465 # For SSL
smtp_server = "smtp.gmail.com"  # Assuming your sender email is Gmail
password = input("Gmail Sender Password: ")
sender_email = "" # If not gmail -- change smtp_server
receiver_email = "" # Any valid email
receiver_text = "PHONENUMBER@txt.att.net"  # Assuming ATT is cell service provider
userID = "" # Discord userID
webhookURL = "" # Discord webhookURL

# Enable / Disable notifications
discord_notification = True
email_notification = True
text_notification = True
console_notification = True

# Email spam limiter
spamLimit = 5 # Max emails & texts it will notify you before stopping notification
spamCounter = 0

# Sends Discord notification
def discord_notify(url):
    message = "<@!" + userID + "> This is in stock now! [Link here](" + url + ")."
    msg = {"content": message}
    requests.post(webhookURL, data=msg) 

# Sends email notification
def email_notify(url):
    global spamCounter
    message = """\
    Subject: StockNotify

    PS5 In Stock Now! """ + url
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    spamCounter += 1

# Sends text notification
def text_notify(url):
    global spamCounter
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_text
    msg['Subject'] = "StockNotify\n"
    body = "PS5 In Stock Now! " + url
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_text, sms)
    spamCounter += 1


# Grabs html from URL
def grab_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content

def check_item_in_stock(page_html, site):
    soup = BeautifulSoup(page_html, 'html.parser')

    if (site == "bestbuy"):
        out_of_stock_divs = soup.findAll("button", {"data-button-state": "SOLD_OUT"})

    if (site == "playstation"):
        out_of_stock_divs = soup.findAll("link", {"href":"https://schema.org/OutOfStock"})

    # FIXME: False positives occasionally.
    # if (site == "amazon"):
        # out_of_stock_divs = soup.find("div", {"id":"availability"})

    # FIXME: Doesn't work. Uses JS to show availability?
    # if (site == "walmart"):
    #     out_of_stock_divs = soup.findAll("Out of stock")
    #     print(out_of_stock_divs)
        
    return len(out_of_stock_divs) == 0

def check(url, site):
    global spamLimit
    global spamCounter
    page_html = grab_html(url)

    # In stock
    if check_item_in_stock(page_html, site):
        # Discord Notification
        if (discord_notification == True):
            discord_notify(url) 

        # Email Notification
        if (email_notification == True and spamCounter <= spamLimit):
            email_notify(url)

        # Text Notification
        if (text_notification == True and spamCounter <= spamLimit):
            text_notify(url)

        # Console Notification
        if (console_notification == True):
            msg = "In stock now! " + url
            print(msg)

    # Out of stock (prints to terminal)
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

# walmartPS5Disk = "https://www.walmart.com/ip/PlayStation-5-Console/363472942?irgwc=1&sourceid=imp_QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&veh=aff&wmlspartner=imp_1943169&clickid=QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383"
# walmartPS5Digital = "https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815?irgwc=1&sourceid=imp_QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&veh=aff&wmlspartner=imp_1943169&clickid=QbA3ga39axyIUPkzIH1IWSTvUkG1aiTAEXYo3E0&sharedid=tomsguide-us&affiliates_ad_id=565706&campaign_id=9383"