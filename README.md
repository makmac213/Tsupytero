python-google-option-chain
==============

$ pip install tsupytero


Sample Usage
============
from tsupytero import Tsupytero

t = Tsupytero()

# get all last trade data (json)
t.all()

# looks for the stock symbol (json)
t.find([symbol])

# gets the latest traded data of a symbol (json)
t.get_latest_data([symbol])

# returns recent (30) days data of a symbol
t.get_recent_data([symbol])

# returns a candlestick chart of the recent 
# (30) days data of a symbol
t.get_recent_candlestick([symbol])

Credits
=======
https://github.com/edgedalmacio/phisix
http://phisix-api.appspot.com/


