import datetime
import requests
from tiingo import TiingoClient


config = {}
config['session'] = True
config['api_key'] = "4a95f4d51a195fdbb87a8f3bc317cffb807f72e4"
client = TiingoClient(config)
now = datetime.datetime.now()

def get_stock_data(ticker: str, period: str = None):
  real_year = int(now.year)
  real_month = int(now.month)
  real_day = int(now.day) - 1
  headers = {
      'Content-Type': 'application/json'
    }
  if period is None:
    print('None')
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}-{}-{}&token=4a95f4d51a195fdbb87a8f3bc317cffb807f72e4".format(ticker, real_year, real_month, real_day), headers=headers)
    requestResponse = requestResponse.json()


  else:
    year = real_year - int(period.split('y')[0])
    month = real_month - int(period.split('m')[0].split('y')[1])
    day = real_day - int(period.split('d')[0].split('m')[1])
    if day < 0:
      day  = 30 + real_day - int(period.split('d')[0].split('m')[1])
    if month < 0:
      day  = 12 + real_day - int(period.split('d')[0].split('m')[1])
    if month < 10:
      month = str(month)
      month = "0" + month
    if day < 10:
      day = str(day)
      day = "0" + day
    print(year, month, day)
    requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}-{}-{}&token=4a95f4d51a195fdbb87a8f3bc317cffb807f72e4".format(ticker, year, month, day), headers=headers)
    requestResponse = requestResponse.json()[0].get("close")
    requestResponse2 = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}-{}-{}&token=4a95f4d51a195fdbb87a8f3bc317cffb807f72e4".format(ticker, real_year, real_month, real_day), headers=headers)
    requestResponse2 = requestResponse2.json()[0].get("close")
    requestResponse3 = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}-{}-{}&endDate={}-{}-{}&token=4a95f4d51a195fdbb87a8f3bc317cffb807f72e4".format(ticker, real_year, real_month, real_day, year, month, day), headers=headers)
    split_counter = 1
    i = 0
    for i in requestResponse3.json():
      split_counter = split_counter * i.get("splitFactor")
    current_price = requestResponse2
    historical_price = requestResponse
    change = current_price * 100 * split_counter / historical_price - 100
    s_change = float('{:.1f}'.format(change))
    if change > 0:
      s_change = str(s_change)
      s_change = '+' + s_change + '%'
    if change < 0:
      s_change = str(s_change)
      s_change = '-' + s_change + '%'
    if change == 0:
      s_change = str(s_change)
      s_change = s_change + '%'
  return s_change
print(year)
ticker = input() 
date = input()
print(get_stock_data(ticker, date))


