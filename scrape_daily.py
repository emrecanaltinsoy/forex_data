import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

today = datetime.date.today()

base_url = "https://www.x-rates.com/historical/?from=USD&amount=1&date"

year = today.year
month = today.month if today.month>9 else f"0{today.month}"
day = today.day if today.day>9 else f"0{today.day}"

URL = f"{base_url}={year}-{month}-{day}"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('tr')[12:]

currencies = [table[i].text.split('\n')[1:3][0] for i in range(len(table))]
currencies.insert(0, "date(y-m-d)")
rates = [table[i].text.split('\n')[1:3][1] for i in range(len(table))]
rates.insert(0, f"{year}-{month}-{day}")
new_row = {currencies[i]: rates[i] for i in range(len(rates))}

df = pd.read_csv("forex_usd_data.csv")
df = df.append(new_row, ignore_index=True)

df.to_csv("forex_usd_data_new.csv",index=None)
