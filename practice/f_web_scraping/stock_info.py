"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_most_active_tickers():
    """Fetches initial tickers from the Most Active list."""
    url = "https://finance.yahoo.com/markets/stocks/most-active/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'lxml')
        tickers = []
        for row in soup.select('table tbody tr'):
            cells = row.find_all('td')
            if len(cells) > 1:
                tickers.append((cells[0].text.strip(), cells[1].text.strip()))
        return tickers
    except Exception as e:
        print(f"Failed to get ticker list: {e}")
        return []

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)
    return driver

def scrape_stock_all_tabs(driver, symbol, name):
    """Navigates through Profile, Statistics, and Holders tabs for a single symbol."""
    data = {
        "Name": name, "Code": symbol, "Country": "N/A", "Employees": "N/A",
        "CEO Name": "N/A", "CEO Year Born": None,
        "52-Week Change": "N/A", "Total Cash": "N/A",
        "Blackrock_Holding": None
    }

    # 1. Profile Tab
    driver.get(f"https://finance.yahoo.com/quote/{symbol}/profile")
    time.sleep(2)
    try:
        address_div = driver.find_element(By.CSS_SELECTOR, "div.address")
        inner_divs = address_div.find_elements(By.TAG_NAME, "div")
        if inner_divs:
            data["Country"] = inner_divs[-1].text.strip()

        stats_list = driver.find_element(By.CSS_SELECTOR, "dl.company-stats")
        stats_text = stats_list.text
        if "Full Time Employees" in stats_text:
            emp_element = stats_list.find_element(By.XPATH,
                                                  ".//dt[contains(., 'Full Time Employees')]/following-sibling::dd/strong")
            data["Employees"] = emp_element.text.strip()

        profile_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        for row in profile_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 5 and "CEO" in cols[1].text:
                data["CEO Name"] = cols[0].text
                data["CEO Year Born"] = cols[4].text if cols[4].text.isdigit() else "N/A"
                break
    except Exception as e:
        print(f"Error scraping Profile for {symbol}: {e}")

    # 2. Statistics Tab
    driver.get(f"https://finance.yahoo.com/quote/{symbol}/key-statistics")
    time.sleep(2)
    try:
        rows = driver.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            if "52 Week Change" in row.text:
                data["52-Week Change"] = row.find_elements(By.TAG_NAME, "td")[1].text
            if "Total Cash" in row.text and "Per Share" not in row.text:
                data["Total Cash"] = row.find_elements(By.TAG_NAME, "td")[1].text
    except: pass

    # 3. Holders Tab
    driver.get(f"https://finance.yahoo.com/quote/{symbol}/holders")
    time.sleep(2)
    try:
        # Find all rows in the institutional holders table
        h_rows = driver.find_elements(By.XPATH, "//table[contains(., 'Date Reported')]//tbody//tr")
        for row in h_rows:
            if "Blackrock" in row.text:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 5:
                    data["Blackrock_Holding"] = {
                        "Name": name,
                        "Code": symbol,
                        "Shares": cols[1].text,
                        "Date Reported": cols[2].text,
                        "% Out": cols[3].text,
                        "Value": cols[4].text
                    }
                break
    except: pass

    return data


def run_report():
    active_stocks = get_most_active_tickers()
    driver = get_driver()
    results = []

    try:
        # Scrape the Most Active stocks
        for symbol, name in active_stocks:
            print(f"Scraping all tabs for: {symbol}...")
            results.append(scrape_stock_all_tabs(driver, symbol, name))

        # --- Rendering Sheets ---

        # Sheet 1
        youngest = sorted([r for r in results if r["CEO Year Born"] and r["CEO Year Born"].isdigit()],
                          key=lambda x: int(x["CEO Year Born"]), reverse=True)[:5]
        render_table("5 stocks with most youngest CEOs", youngest,
                     ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"])

        # Sheet 2
        def parse_pct(s):
            try:
                return float(s.replace('%', '').replace(',', '').replace('+', ''))
            except:
                return -999.0

        best_gainers = sorted(results, key=lambda x: parse_pct(x["52-Week Change"]), reverse=True)[:10]
        render_table("10 stocks with best 52-Week Change", best_gainers,
                     ["Name", "Code", "52-Week Change", "Total Cash"])

        # Sheet 3
        blackrock_stakes = [r["Blackrock_Holding"] for r in results if r["Blackrock_Holding"]]

        def parse_percent(val):
            try:
                return float(val.replace('%', '').strip())
            except:
                return 0.0

        blackrock_stakes = sorted(blackrock_stakes, key=lambda x: parse_percent(x["% Out"]), reverse=True)[:10]

        render_table("10 most active stocks with largest Blackrock Inc. holdings", blackrock_stakes,
                     ["Name", "Code", "Shares", "Date Reported", "% Out", "Value"])

    finally: driver.quit()

def render_table(title, rows, fields):
    print(f"\n{title.center(100, '=')}")
    if not rows:
        print("| No data found.")
        return
    widths = {f: max(len(f), max(len(str(r.get(f, ""))) for r in rows)) for f in fields}
    sep = "-" * (sum(widths.values()) + (len(fields) * 3) + 1)
    print("| " + " | ".join(f"{f:<{widths[f]}}" for f in fields) + " |")
    print(sep)
    for r in rows:
        print("| " + " | ".join(f"{str(r.get(f, '')):<{widths[f]}}" for f in fields) + " |")
    print("")

if __name__ == "__main__":
    run_report()
