import alpaca_trade_api as tradeapi
import threading
import time
import datetime

from handel import util

API_KEY = "YOUR_API_KEY_HERE"
API_SECRET = "YOUR_API_SECRET_HERE"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

TARGET_POSITION_SIZE = 200
MIN_POSITION_SIZE = 50

class Status:
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

def run_day(status):
  # Wait till 30 mins before market open to load csv.
  util.await_market_open(status.alpaca, 30)
  data = util.load_csv()

  # Cancel previous orders
  # orders = status.alpaca.list_orders(status="open")
  # for order in orders:
  #     status.alpaca.cancel_order(order.id)

  # Sort the predictions by the expected discounted return of each stock (do you have this??)
  data = data.sort_values(by=['expected_return'])
  # Attempt to allocate as close to POSITION_SIZE as possibe for the top stocks.
  # TODO: at least weight this by the expectation or something.

  for row in data.itertuples():
    if status.cash < MIN_POSITION_SIZE:
      print('Ran out of money for opening positions')
    qty = TARGET_POSITION_SIZE // row.limit
    try:
      alpaca.submit_order(symbol=row.symbol,
                          qty=qty,
                          side='buy',
                          type='limit',
                          order_class="bracket",
                          time_in_force="gtc",
                          limit_price=row.limit,
                          take_profit={'limit_price': row.take_profit},
                          stop_loss={'stop_price': row.stop,
                                     'limit_price': row.stop_limit})
      print("Order for {} for {}$ at {}$, profit at {}, stop/limit at {}/{} completed.".format(row.symbol,
                                                                                               qty*row.limit,
                                                                                               row.take_profit,
                                                                                               row.stop,
                                                                                               row.stop_limit))
    except:
      print("ERROR: Order for {} for {}$ at {}$, profit at {}, stop/limit at {}/{} failed.".format(row.symbol,
                                                                                               qty*row.limit,
                                                                                               row.take_profit,
                                                                                               row.stop,
                                                                                               row.stop_limit))

  if status.cash >= MIN_POSITION_SIZE:
    print('Ran out of positions to open')

  # Print summaries every hour.
  while alpaca.get_clock_is_open():
    util.summarize()
    time.sleep(3600)

  # Summarize once more end-of-day.
  util.summarize()

def main():
  status = Status()
  days_running = 0
  while True:
    print('Good morning! This script has been trading for {} days'.format(days_running))
    run_day(status)
