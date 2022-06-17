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
  if date is None:
    print('None')
    historical_prices = client.get_ticker_price("{}".format(ticker),
                                                fmt='json',
                                                startDate='{}-{}-{}'.format(real_year, real_month, real_day),
                                                endDate='{}-{}-{}'.format(real_year, real_month, real_day),
                                                frequency='daily')

  else:
    year = int(date.split('.')[0])
    month = int(date.split('.')[1])
    day = int(date.split('.')[2])
    historical_prices = client.get_ticker_price("{}".format(ticker),
                                                fmt='json',
                                                startDate='{}-{}-{}'.format(year, month, day),
                                                endDate='{}-{}-{}'.format(year, month, day),
                                                frequency='daily')
    
  return historical_prices

ticker = input()
date = input()
print(get_stock_price_by_date(ticker,date))


