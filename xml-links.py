import requests
from lxml import etree
import json

# url = "https://www.dailyamardesh.com/sitemaps/news-sitemap.xml"
# url = "https://www.dhakatribune.com/2025-12-01.xml"
# url = "https://www.jugantor.com/news_sitemap.xml"
# url = "https://www.thedailystar.net/sitemap.xml?page=109"
# url = "https://www.banglatribune.com/archive_2025-12-01.xml"
url = "https://www.kalerkantho.com/daily-sitemap/2025-06-29/sitemap.xml"

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

root = etree.fromstring(response.content)

# Namespaces
ns = {
    "ns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "news": "http://www.google.com/schemas/sitemap-news/0.9"
}

data = []

for url_elem in root.findall("ns:url", ns):
    loc = url_elem.find("ns:loc", ns)
    lastmod = url_elem.find("ns:lastmod", ns)

    news = url_elem.find("news:news", ns)

    item = {
        "url": loc.text if loc is not None else None,
        "lastmod": lastmod.text if lastmod is not None else None,
        "publication_name": None,
        "language": None,
        "publication_date": None,
        "title": None,
        "keywords": None
    }

    if news is not None:
        item["publication_name"] = news.findtext(
            "news:publication/news:name", namespaces=ns
        )
        item["language"] = news.findtext(
            "news:publication/news:language", namespaces=ns
        )
        item["publication_date"] = news.findtext(
            "news:publication_date", namespaces=ns
        )
        item["title"] = news.findtext(
            "news:title", namespaces=ns
        )
        item["keywords"] = news.findtext(
            "news:keywords", namespaces=ns
        )

    data.append(item)

print(json.dumps(data, indent=2, ensure_ascii=False))
