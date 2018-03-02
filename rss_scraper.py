import requests
from bs4 import BeautifulSoup

url = "rss feed"

response = requests.get(url)

soup = BeautifulSoup(response.content, features = "xml")

items = soup.find_all("item")

for item in items:
    item.title.text
    # etc.