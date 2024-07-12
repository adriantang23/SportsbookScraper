from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from urllib.parse import urljoin

import time
import random

pinny = "https://www.pinnacle.com"

# Headless driver as precaution for getting blocked while scraping
def headlessDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# Get matchup links to be used in getPP()
def getMatchups(url):
    driver = headlessDriver()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.contentBlock')))
    time.sleep(5)
    source = driver.page_source
    driver.quit()

    parsed = BeautifulSoup(source, 'html.parser')
    matchups = parsed.find_all('div', class_='style_row__yBzX8 style_row__12oAB')

    URL = []
    for matchup in matchups:
        atag = matchup.find('a', href=True)
        if atag:
            href = atag['href']
            ppSub = urljoin(href, '#player-props')
            full_url = urljoin(pinny, ppSub)
            URL.append(full_url)

    print(f"Found {len(URL)} matchups")
    return URL

# Get Player props, lines, and odds
def getPP(url):
    driver = headlessDriver()
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-collapsed="false"]')))
    except Exception as e:
        print(f"Error locating element in {url}: {e}")
        driver.quit()
        return ""

    source = driver.page_source
    driver.quit()

    parsed = BeautifulSoup(source, 'html.parser')
    player_props = parsed.find_all('div', attrs={"data-collapsed": "false"})

    scraped = {}
    for player in player_props:
        name_span = player.find('span', class_='style_titleText__2NaZn')
        if name_span:
            player_name = name_span.text.strip()
            lines_odds = []
            buttons = player.find_all('button', class_='market-btn')
            for button in buttons:
                line = button.find('span', class_='style_label__3BBxD').text.strip()
                odds = button.find('span', class_='style_price__3Haa9').text.strip()
                lines_odds.append((line, odds))
            scraped[player_name] = lines_odds

    final = ''
    for key, value in scraped.items():
        final += f"{key}:\n"
        for item in value:
            final += f"  {item}\n"
    
    print(f"Scraped data from {url}")
    return final

# Input sport category to find all player props of all matchups
def scraper(url, txt):
    matchups = getMatchups(url)
    with open(txt, 'w', encoding='utf-8') as file:
        for matchup in matchups:
            Props = getPP(matchup)
            file.write(Props + '\n')
            file.flush()
            time.sleep(random.uniform(1, 5))
    print('All Done!')

# # test case for gathering player prop lines and odds
# print(getPP('https://www.pinnacle.com/en/baseball/mlb/san-francisco-giants-vs-cleveland-guardians/1593450019/#player-props'))

# # test case for gathering matchups
# print(getMatchups('https://www.pinnacle.com/en/baseball/matchups/'))

baseball_url = 'https://www.pinnacle.com/en/baseball/matchups/'
baseball_txt = 'baseball.txt'
scraper(baseball_url, baseball_txt)

soccer_url = 'https://www.pinnacle.com/en/soccer/matchups/highlights/'
soccer_txt = 'soccer.txt'
# scraper(soccer_url,soccer_txt)

#tennis has good 'Total Games' value
