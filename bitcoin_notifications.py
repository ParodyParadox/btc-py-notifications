import requests
import time
from datetime import datetime
#EVENTS:
#bitcoin_price_update
#bitcoin_price_emergency

btc_price_threshhold = 10000 # set to whatever

btc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
ifttt_update_url = 'https://maker.ifttt.com/trigger/{}/with/key/UF2UaOh18WmIYh1_fQ1ko'
def get_latest_btc_price():
    parameters = {
    'id':'1',
    'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '9132bf27-a483-413a-8732-2dfe8e6f3045',
    }
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(btc_url, params=parameters)
    response_json = response.json()
    return round(float(response_json['data']['1']['quote']['USD']['price']))

def post_ifttt_webhook(event, value):
    data = {'value1':value}
    ifttt_event_url = ifttt_update_url.format(event)
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
    bitcoin_history = []
    while True:
        price = get_latest_btc_price()
        date = datetime.now()
        bitcoin_history.append({'date':date, 'price':price})

        if price < btc_price_threshhold:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            bitcoin_history = []

        time.sleep(60 * 5)

if __name__ == '__main__':
    main()
