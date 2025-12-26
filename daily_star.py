import json
import requests
from bs4 import BeautifulSoup
import time
import os

INPUT_FILE = "daily_star_links.json"
OUTPUT_FILE = f"daily_star_articles_with_body_{time.strftime('%Y%m%d_%H%M%S')}.json"
ERROR_LOG = "errors.log"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

DELAY = 1  # seconds


def load_json_safe(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json_safe(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)  # atomic write


articles = load_json_safe(INPUT_FILE, [])
results = load_json_safe(OUTPUT_FILE, [])

# Track already-scraped URLs (resume support)
done_urls = {item["url"] for item in results if "url" in item}

print(f"Loaded {len(articles)} input URLs")
print(f"Resuming from {len(done_urls)} already scraped articles")

for idx, item in enumerate(articles, start=1):
    url = item.get("url")

    if not url or url in done_urls:
        continue

    print(f"[{idx}/{len(articles)}] Fetching: {url}")

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Headline
        headline_el = soup.select_one('.fw-700.e-mb-16.article-title')
        headline = headline_el.get_text(strip=True) if headline_el else item.get("title")


        # Article body (primary + fallback)
        paragraphs = soup.select('.pb-20.clearfix p')
        body_text = " ".join(
            p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
        )


        result = {
            "url": url,
            "title": headline,
            "publication_date": item.get("publication_date"),
            "keywords": item.get("keywords"),
            "body": body_text,
            "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%S")
        }

        results.append(result)
        save_json_safe(OUTPUT_FILE, results)
        done_urls.add(url)

        print("  ✔ Saved")

    except Exception as e:
        print(f"  ✖ Failed: {e}")

        with open(ERROR_LOG, "a", encoding="utf-8") as f:
            f.write(f"{url}\t{str(e)}\n")

    time.sleep(DELAY)

print(f"\nDone. Total saved articles: {len(results)}")
