import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

start_date = datetime.date(2011, 1, 1)
today = datetime.date.today()
date_delta = today - start_date
date_list = [today - datetime.timedelta(days=x) for x in range(date_delta.days, -1, -1)]

base_url = "https://www.x-rates.com/historical/?from=USD&amount=1&date"

run_once = True

for date in date_list:
    year = date.year
    month = date.month if date.month > 9 else f"0{date.month}"
    day = date.day if date.day > 9 else f"0{date.day}"

    URL = f"{base_url}={year}-{month}-{day}"

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find_all("tr")[12:]

    if run_once:
        currencies = [table[i].text.split("\n")[1:3][0] for i in range(len(table))]
        currencies.insert(0, "date(y-m-d)")
        rates = [table[i].text.split("\n")[1:3][1] for i in range(len(table))]
        rates.insert(0, f"{year}-{month}-{day}")
        data = {currencies[i]: rates[i] for i in range(len(rates))}
        df = pd.DataFrame(data, index=[0])
        run_once = False
    else:
        rates = [table[i].text.split("\n")[1:3][1] for i in range(len(table))]
        rates.insert(0, f"{year}-{month}-{day}")
        new_row = {currencies[i]: rates[i] for i in range(len(rates))}
        df = df.append(new_row, ignore_index=True)

    print(date)

df.to_csv("forex_usd_data.csv", index=None)
