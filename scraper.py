import requests
from bs4 import BeautifulSoup
from datetime import datetime

# RSS Feed URL
rss_url = "https://mashable.com/feed/"

# Fetch RSS
response = requests.get(rss_url)
soup = BeautifulSoup(response.content, features="xml")

# Find all items (articles)
items = soup.find_all('item')

# Loop through articles
for item in items:
    title = item.title.text
    link = item.link.text
    pub_date_str = item.pubDate.text

    # Parse date string
    pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')


    # Filter by date >= 2022-01-01
    from datetime import timezone

filter_date = datetime(2022, 1, 1, tzinfo=timezone.utc)

if pub_date >= filter_date:
    print(f"{pub_date} - {title} -> {link}")

