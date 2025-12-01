import nest_asyncio
nest_asyncio.apply()
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    firefox = pw.firefox.launch(headless=False)
    page = firefox.new_page()
    url = "https://www.metal-archives.com/bands/Brad_Jurjens/3540460030"
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

print(genre)
print(formed)
print(years)
print(location)
print(releases)