from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

parse_table = []
for date in range(4, 9):
    html = urlopen('https://www.nasdaq.com/earnings/daily-earnings-surprise.aspx?reportdate=2019020'+str(date))
    soup = BeautifulSoup(html.read(), "lxml")
    table_list = soup.findAll('table')
    if len(table_list)==3:
        for i in range(3):
            table = table_list[i]
            rows = table.findAll("tr")
            if len(rows)>1:
                for row in rows:
                    cells = row.findAll("td")
                    if len(cells)>0:
                        name = cells[0].findAll('a')[0].find(text=True)
                        ticker = cells[0].findAll('h3')[0].findAll('a')[0].find(text=True)
                        fiscal_quarter = cells[1].find(text=True)
                        eps = cells[2].find(text=True)
                        eps_forecast = cells[3].find(text=True)
                        num_ests = cells[4].find(text=True)
                        pct_surprise = cells[5].find(text=True)
                        parse_table.append([date, ticker, name, fiscal_quarter, eps, eps_forecast, num_ests, pct_surprise])


earnings_surprise = pd.DataFrame(parse_table)
earnings_surprise.columns = [['Report Date', 'Ticker', 'Name', 'Fiscal Quarter Reported',
                             'EPS', 'EPS Forecast', '#Ests', '%Surprise']]
print(earnings_surprise)

