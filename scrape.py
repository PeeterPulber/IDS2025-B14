import nest_asyncio
nest_asyncio.apply()
from playwright.sync_api import sync_playwright

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
        year = cells[2].inner_text()
        releases.append(year)

    return {"genre": genre, "formed": formed, "years": years, "location": location, "releases": releases}

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=False)
    page = browser.new_page()
    url = "https://www.metal-archives.com/lists/EE"
    page.goto(url)
    page.wait_for_selector("table.display.dataTable tbody tr")
    rows = page.query_selector_all("table.display.dataTable tbody tr")
    links = []
    for row in rows:
        link = row.query_selector("td.sorting_1 a").get_attribute("href")
        links.append(link)
    print(links)