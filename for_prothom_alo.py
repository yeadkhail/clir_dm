import requests
from lxml import etree
import json

# --- CHANGE THIS to your sitemap URL ---
url = "https://www.prothomalo.com/sitemap/sitemap-daily-2025-12-25.xml"

# --- Fetch sitemap ---
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
response.raise_for_status()
root = etree.fromstring(response.content)

# --- Namespaces ---
ns = {
    "ns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "news": "http://www.google.com/schemas/sitemap-news/0.9",
    "image": "http://www.google.com/schemas/sitemap-image/1.1"
}

data = []

# --- Iterate over each <url> entry ---
for url_elem in root.findall("ns:url", ns):
    item = {
        "url": url_elem.findtext("ns:loc", namespaces=ns),
        "lastmod": url_elem.findtext("ns:lastmod", namespaces=ns),
        "publication_name": None,
        "language": None,
        "publication_date": None,
        "title": None,
        "keywords": None,
    }

    # --- Google News sitemap metadata ---
    news = url_elem.find("news:news", ns)
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

    # --- Image sitemap (Prothom Alo) ---
    images = []
    for img in url_elem.findall("image:image", ns):
        images.append({
            "url": img.findtext("image:loc", namespaces=ns),
            "caption": img.findtext("image:caption", namespaces=ns)
        })

    if images:
        item["images"] = images

    data.append(item)

# --- Output JSON ---
print(json.dumps(data, indent=2, ensure_ascii=False))
