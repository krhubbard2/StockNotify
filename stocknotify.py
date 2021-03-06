# stocknotify.py
# Kelby Hubbard
# Started: 2022-01-06
# Updated: 2022-01-10

# Notify a user via Discord, email, or sms text of potential item in stock using Discord webhook, html parsing and smtplib. Currently works with Bestbuy, Playstation direct and Gamestop.

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
    message = "<@!" + userID + "> Item in stock now! [Link here](" + url + ")."
    msg = {"content": message}
    requests.post(webhookURL, data=msg) 

# Sends email notification
def email_notify(url):
    global spamCounter
    message = """\
    Subject: StockNotify

    Item in stock now! """ + url
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
    body = "Item in stock now! " + url
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

    if (site == "gamestop"):
        out_of_stock_divs = soup.findAll("div", {"data-ready-to-order": "false"})

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
    gamestopDigital = "https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/sony-playstation-5-digital-edition-console/11108141.html?bt=true"
    gamestopDisk = "https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/sony-playstation-5-console/11108140.html?bt=true"

    # Currently working websites (used to tell check function which site you're tracking)
    websites = ["bestbuy", "playstation", "gamestop"]
 
    while True:
        # check(URL, website)
        check(bestbuyPS5Disk, websites[0])
        check(bestbuyPS5Digital, websites[0])
        check(playstationDigital, websites[1])
        check(playstationDisk, websites[1])
        check(gamestopDigital, websites[2])
        check(gamestopDisk, websites[2])

        # To reduce unnecessary spamming of websites, ensure a sleep time of 60 seconds.
        time.sleep(60)

main()