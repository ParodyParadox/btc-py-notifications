import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time

btc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
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

try:
    response = session.get(btc_url, params=parameters)
    data = json.loads(response.text)
    #print(data)
    price = data['data']['1']['quote']['USD']['price']
    price = round(float(price), 2)
    print(price)
    time.sleep(1440)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
time.sleep(1000)
