# -*- encoding: utf-8 -*-
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def accept_terms():
    accept_button = driver.find_element_by_id('onetrust-accept-btn-handler')
    accept_button.click()
    return


def build_rank(type):
    field = rankings[type]['field']
    label = rankings[type]['label']

    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element_by_xpath(
        "//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    return df.to_dict('records')


option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)
driver.get(url)
driver.implicitly_wait(10)

accept_terms()
time.sleep(10)

for k in rankings:
    top10ranking[k] = build_rank(k)

driver.quit()

with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)
