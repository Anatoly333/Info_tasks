import datetime
from tiingo import TiingoClient


config = {}
config['session'] = True
config['api_key'] = "4a95f4d51a195fdbb87a8f3bc317cffb807f72e4"
client = TiingoClient(config)
now = datetime.datetime.now()

def get_stock_price_by_date(ticker: str, date: str = None):
  real_year = int(now.year)
  real_month = int(now.month)
  real_day = int(now.day)
  if date == '':
    historical_prices = client.get_ticker_price("{}".format(ticker),
                                                fmt='json',
                                                startDate='{}-{}-{}'.format(real_year, real_month, real_day),
                                                endDate='{}-{}-{}'.format(real_year, real_month, real_day),
                                                frequency='daily')

  else:
    year = int(date.split('y')[0])
    month = int(date.split('m')[0].split('y')[1])
    day = int(date.split('d')[0].split('m')[1])
    historical_prices = client.get_ticker_price("{}".format(ticker),
                                                fmt='json',
                                                startDate='{}-{}-{}'.format(year, month, day),
                                                endDate='{}-{}-{}'.format(year, month, day),
                                                frequency='daily')
    
  return historical_prices

import datetime
def get_historical_date_by_period(period: str):
  #raise NotImplementedError
  now = datetime.datetime.now()

  year = int(period.split('y')[0])
  month = int(period.split('m')[0].split('y')[1])
  day = int(period.split('d')[0].split('m')[1])

  real_year = int(now.year)
  real_month = int(now.month)
  real_day = int(now.day)

  new_year = real_year - year
  new_month = real_month - month
  new_day = real_day - day
  new_date = str(new_year) + 'y' + str(new_month) + 'm' + str(new_day) + 'd'
  return new_date



def get_price_change(historical_price: float, current_price: float) -> float:
  current_price = int(current_price)
  historical_price = int(historical_price)
  change = ((current_price - historical_price)/historical_price)*100
  return change
hustory_price = input()
current_price = input()
print(get_price_change(hustory_price, current_price),'%')
period = input()
print(get_historical_date_by_period(period))


ticker = input()
date = input()
print(get_stock_price_by_date(ticker,date))
