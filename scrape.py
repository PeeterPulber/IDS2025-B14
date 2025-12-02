import nest_asyncio
nest_asyncio.apply()
from playwright.sync_api import sync_playwright
import json
import time
import os

def load_urls(filename):
    urls = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    urls.add(json.loads(line)["url"])
    return urls

def scrape_band(page,url):
    page.goto(url)
    page.wait_for_selector("table.display.discog tbody")

    genre = page.query_selector("dl.float_right dd").inner_text()
    formed = page.query_selector("dl.float_left dd:nth-of-type(4)").inner_text()
    years = page.query_selector("dl.clear dd").inner_text()
    location = page.query_selector("dl.float_left dd:nth-of-type(2)").inner_text()

    releases_rows = page.query_selector_all("table.display.discog tbody tr")
    releases = []
    for row in releases_rows:
        cells = row.query_selector_all("td")
        if len(cells) == 1: # No releases
            break
        year = cells[2].inner_text()
        releases.append(year)

    return {"url": url, "genre": genre, "formed": formed, "years": years, "location": location, "releases": releases}

def save_band(line, filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

url = "https://www.metal-archives.com/lists/EE"
filename = "bandsEE.jsonl"
scraped = load_urls(filename)

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector("table.display.dataTable tbody tr")
    rows = page.query_selector_all("table.display.dataTable tbody tr")
    links = []

    for band in rows:
        link = band.query_selector("td.sorting_1 a").get_attribute("href")
        links.append(link)

    for link in links:
        if link not in scraped:
            time.sleep(3)
            save_band(scrape_band(page,link), filename)

    browser.close()

print("Finished scraping")