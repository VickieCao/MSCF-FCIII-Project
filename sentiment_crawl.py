from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd

html = urlopen('http://sentdex.com/financial-analysis/?tf=all')
soup = BeautifulSoup(html.read(), "lxml")
table_list = soup.findAll('table')
senti_table = table_list[0]
rows = senti_table.findAll("tr")

parse_table = []
for row in rows:
    cells = row.findAll("td")
    if len(cells)>0:
        ticker = cells[0].find(text=True)
        name = cells[1].find(text=True)
        volume = cells[2].find(text=True)
        sentiment = cells[3].find(text=True)
        str_up_down = str(cells[4].findAll('span')[0])
        rise_fall = re.findall(r'down|up', str_up_down)[0]
        newr = [ticker, name, volume, sentiment, rise_fall]
        parse_table.append(newr)


sentdex = pd.DataFrame(parse_table)
sentdex.columns = [['Ticker', 'Name', 'Volume of Mention', 'Sentiment', 'Rising or Falling']]
print(sentdex)
sentdex.to_excel('data_sample.xlsx')

