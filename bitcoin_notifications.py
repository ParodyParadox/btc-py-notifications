import requests
import config
from tkinter import *
import time
from datetime import datetime
import threading
#EVENTS:
#bitcoin_price_update
#bitcoin_price_emergency

tk = Tk()
tk.geometry('500x300')
tk.resizable(0,0)
tk.title('Bitcoin Notification Control Panel')

Label(tk, text='Control Panel', font='arial 20 bold').pack()
status = Label(tk, text='Status: Off', font='arial 20 bold')
status.pack(side='bottom')

btc_price_threshhold = 10000 # set to whatever
history_before_send = 5

run = False

btc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
ifttt_update_url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
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

def Off():
    global run
    status.config(text='Status: Off')
    run = False

def On():
    global run
    if run == False:
        run = True
        status.config(text='Status: On')
        threading.Thread(target=main).start()
    else:
        pass

def Exit():
    tk.destroy()

def main():
    global run
    bitcoin_history = []
    while run:
        print('running')
        price = get_latest_btc_price()
        date = datetime.now()
        bitcoin_history.append({'date':date, 'price':price})

        if price < btc_price_threshhold:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_history) == history_before_send:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            bitcoin_history = []
        if run:
            time.sleep(60 * 5)
        else:
            break
    print('stopped')

Button(tk, text='START', font='arial 16 bold', command=On, padx=10, width=12, height=5, bg='green').pack(side='left')
Button(tk, text='STOP', font='arial 16 bold', command=Off, padx=10, width=12, height=5, bg='red').pack(side='right')
Button(tk, text='EXIT', font='arial 10 bold', command=Exit, padx=2, width=8, height=2, bg='ghost white').pack(side='bottom')

tk.mainloop()
