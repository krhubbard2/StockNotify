# StockNotify
PS5 restock notifier via Discord webhook and BeautifulSoup.

## Pre-Requisites:
Requests  
beautifulsoup4

## Install, Setup & Configuration:
Clone repository.
Enable or disable whichever notifications you'd like (Lines 24-27).  
Input Discord userID of user you'd like mentioned on notification in "userID".  
Input Discord webhookURL in "webhookURl"  
Input sender_email -- If email is sent from something other than gmail you must change the smtp_server also.  
Input receiver_email.  
Input receiver_text -- 9 digit phone number followed by cell service carriers email.  
  
spamLimit default set to 5. If item is in stock for prolonged periods you could potentially receive and email/text every 15 seconds. I don't recommend removing this limit.  
  
Run program and enter email sender password. If you're just doing Discord notification simply press "enter".  

## Current Features:
Currently scans Bestbuy.com (digital and disk) and PlayStation Direct (digital and disk).   
Will alert via Discord notification, email, or text message.  

## Features To Come:
More website support (Amazon & Walmart)  
