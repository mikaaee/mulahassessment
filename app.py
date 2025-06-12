from flask import Flask, render_template, request, send_from_directory
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

def get_articles():
    rss_url = "https://mashable.com/feed/"
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.content, features="xml")
    items = soup.find_all('item')

    articles = []
    filter_date = datetime(2022, 1, 1, tzinfo=timezone.utc)

    for item in items:
        title = item.title.text
        link = item.link.text
        pub_date_str = item.pubDate.text
        pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')

        if pub_date >= filter_date:
            articles.append({
                'title': title,
                'link': link,
                'date': pub_date
            })

    # Sort anti-chronologically (latest first)
    articles.sort(key=lambda x: x['date'], reverse=True)

    return articles

@app.route("/")
def home():
    search_query = request.args.get('q', '').lower()
    articles = get_articles()

    if search_query:
        articles = [article for article in articles if search_query in article['title'].lower()]

    return render_template("index.html", articles=articles, search_query=search_query)

if __name__ == "__main__":
    app.run(debug=True)
