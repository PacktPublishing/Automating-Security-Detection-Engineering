#!/usr/bin/env python3
import feedparser
from datetime import datetime, timedelta

#variables
url = "https://allinfosecnews.com/feed/"
feed = feedparser.parse(url)
links = []

#set time and date boundaries to calc
now = datetime.now()
time_range = timedelta(days=1)

for entry in feed.entries:
  #have to remove the offset because of striptimes parameters
  entry_date_str = entry.published[:-6]
  entry_date = datetime.strptime(entry_date_str, "%a, %d %b %Y %H:%M:%S")

  if now - entry_date <= time_range:
    links.append(entry.link)
#print(type(links))
print(links)
