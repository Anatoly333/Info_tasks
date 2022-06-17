from bs4 import BeautifulSoup
import requests as req
    
resp = req.get("https://www.banki.ru/products/currency/cash/usd/sankt-peterburg/")
 
soup = BeautifulSoup(resp.text, 'lxml')
print(soup.title)
#for link in soup.find_all('data-currencies-rate-sell'):
 #   print (link.get('href'))
a = soup.find('div', 'data-currencies-rate-sell')
print(a)