import requests
from functions import *
import config
from tkinter import *
import time
from datetime import datetime
import threading

def get_latest_btc_price():
    parameters = {
    'id':'1',
    'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': config.coinmarketcap_api_key,
    }
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(btc_url, params=parameters)
    response_json = response.json()
    return round(float(response_json['data']['1']['quote']['USD']['price']))

def post_ifttt_webhook(event, value):
    data = {'value1':value}
    ifttt_event_url = ifttt_update_url.format(event, config.ifttt_api_key)
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for btc_price in bitcoin_history:
        date = btc_price['date'].strftime('%d.%m.%Y %H:%M')
        price = btc_price['price']

        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)

def main():
    print('running')
    bitcoin_history = []
    #while True:
    price = get_latest_btc_price()
    date = datetime.now()
    bitcoin_history.append({'date':date, 'price':price})

    if price < btc_price_threshhold:
        post_ifttt_webhook('bitcoin_price_emergency', price)

    if len(bitcoin_history) == history_before_send:
        post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
        bitcoin_history = []

    #time.sleep(60 * 5)
