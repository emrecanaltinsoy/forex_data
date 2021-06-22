import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

today = datetime.date.today()

base_url = "https://www.x-rates.com/historical/?from=USD&amount=1&date"

df = pd.read_csv("forex_usd_data.csv")
last_year, last_month, last_day = [
    int(val) for val in df.iloc[-1, :]["date(y-m-d)"].split("-")
]

date_range = pd.date_range(
    start=df.iloc[-1, :]["date(y-m-d)"], end=f"{today.year}-{today.month}-{today.day}"
)

for dt in date_range[1:-1]:
    y = dt.year
    m = f"0{dt.month}" if dt.month <= 9 else dt.month
    d = f"0{dt.day}" if dt.day <= 9 else dt.day

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
