import requests
from lxml import etree
import json

url = "https://www.kalerkantho.com/daily-sitemap/2025-06-29/sitemap.xml"

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

parser = etree.XMLParser(recover=True)  # recover=True will ignore undefined entities
root = etree.fromstring(response.content, parser=parser)

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
        publication = news.find("news:publication", ns)
        if publication is not None:
            name = publication.find("news:name", ns)
            language = publication.find("news:language", ns)
            item["publication_name"] = name.text if name is not None else None
            item["language"] = language.text if language is not None else None

        pub_date = news.find("news:publication_date", ns)
        title = news.find("news:title", ns)
        keywords = news.find("news:keywords", ns)
        item["publication_date"] = pub_date.text if pub_date is not None else None
        item["title"] = title.text if title is not None else None
        item["keywords"] = keywords.text if keywords is not None else None

    data.append(item)

print(json.dumps(data, indent=2, ensure_ascii=False))
