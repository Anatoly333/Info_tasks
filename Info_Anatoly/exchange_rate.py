"""Кабанов"""
import requests
from bs4 import BeautifulSoup
def best_exchange_rate(currency_code, num_branches):
    list_with_tuple = []
    container = 'exchange-calculator-rates table-flex__row-group'
    green_container = "exchange-calculator-rates table-flex__row-group row-bg-green-bordered"
    dark_text = "table-flex__cell table-flex__rate font-size-large color-border-dark text-nowrap"
    normal_text =  'table-flex__cell table-flex__rate font-size-large text-nowrap'
    orange_text = "table-flex__cell table-flex__rate font-size-large color-pumpkin-orange text-nowrap"
    attr = 'data-currencies-rate-sell'
    url_with_name = "font-size-default color-gray-gray"
    container_with_pr= "table-flex__row item calculator-hover-icon__container"
    url = "https://www.banki.ru/products/currency/cash/"+currency_code+"/sankt-peterburg"

    page = requests.get(url)
    content = BeautifulSoup(page.text, "html.parser")
    for data in content.find_all('div', class_=container):
        filial = data.find('a', class_="font-bold").contents[0]
        bank = data.find('a', class_=url_with_name).contents[0]
        sell_pr_cont = data.find('div', class_=container_with_pr)
        sell_pr_div = sell_pr_cont.find('div', class_=normal_text, attrs={attr:True})
        if sell_pr_div is  None:
            sell_pr_div = sell_pr_cont.find('div', class_=orange_text, attrs={attr:True})
            if  sell_pr_div is None:
                sell_pr_div = sell_pr_cont.find('div', class_=dark_text, attrs={attr:True})
        sell_price = sell_pr_div['data-currencies-rate-sell']
        list_with_tuple.append((bank, filial, round(float(sell_price), 2)))

    list_with_tuple.sort(key=lambda tup: tup[2], reverse=True)
    if num_branches <= 0:
        raise IndexError('Нельзя вводить числа <= 0')
    elif len(list_with_tuple) < num_branches:
        raise IndexError('Вы ввели слишком большое число')
															
    return list_with_tuple[0:num_branches]
