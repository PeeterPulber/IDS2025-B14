import nest_asyncio
nest_asyncio.apply()
from playwright.sync_api import sync_playwright


pw = sync_playwright().start()
firefox = pw.firefox.launch(headless=False)
page = firefox.new_page()
page.goto("https://www.metal-archives.com/bands/Aeon_Aethereal/3540258444")
page.wait_for_selector("dl.float_right dd")

genre = page.query_selector("dl.float_right dd").inner_text()
years = page.query_selector("dl.clear dd").inner_text()
location = page.query_selector("dl.float_left dd:nth-of-type(2)").inner_text()
print(genre)
print(years)
print(location)