import time
import pandas

from datetime import date

CSV_FILE_LOCATION = "fix me"

def time_to_open(alpaca):
  clock = alpaca.get_clock()
  opening_time = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
  curr_time = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
  return (opening_time - curr_time) / 60

# Wait for market to open, or offset minutes before that.
def await_market_open(alpaca, offset=0):
  is_open = alpaca.get_clock().is_open
  while not is_open:
    tto = time_to_open(alpaca)
    if offset != 0 and tto <= offset:
      return
    print(str(tto) + "{} minutes til market open.".format(tto))
    time.sleep(60)
    is_open = alpaca.get_clock().is_open

def load_csv():
  return pandas.readcsv(CSV_FILE_LOCATION)

def summarize(alpaca):
  print('Today is {} {}.'.format(date.today.strftime('%A'), date.today()))
  print('You have {} total value with {} in stocks and {} in cash'.format(alpaca.equity,
                                                                          alpaca.equity - alpaca.cash,
                                                                          alpaca.cash))
  print('Your current positions are:')
  positions = self.alpaca.list_positions()
  positions.sort(key=lambda pos: pos.market_value)
  for pos in positions:
    print('{} : {}$, Total gain: {}. Gain today: {}.'.format(pos.symbol,
                                                             pos.market_value,
                                                             pos.unrealized_plpc,
                                                             pos.unrealized_intraday_plpc))
