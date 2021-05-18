import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

today = datetime.date.today()

base_url = "https://www.x-rates.com/historical/?from=USD&amount=1&date"

df = pd.read_csv("forex_usd_data.csv")
last_year, last_month, last_day = [int(val) for val in df.iloc[-1,:]["date(y-m-d)"].split("-")]

year = today.year
month = today.month
day = today.day

for y in range(last_year, year+1):
    for m in range(last_month, month+1):
        m = f"0{m}" if m < 9 else m
        for d in range(last_day+1, day):
            d = f"0{d}" if d < 9 else d
            
            URL = f"{base_url}={y}-{m}-{d}"

            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")

            table = soup.find_all("tr")[12:]

            currencies = [table[i].text.split("\n")[1:3][0] for i in range(len(table))]
            currencies.insert(0, "date(y-m-d)")
            rates = [table[i].text.split("\n")[1:3][1] for i in range(len(table))]
            rates.insert(0, f"{y}-{m}-{d}")
            new_row = {currencies[i]: rates[i] for i in range(len(rates))}

            df = df.append(new_row, ignore_index=True)

df.to_csv("forex_usd_data.csv", index=None)
