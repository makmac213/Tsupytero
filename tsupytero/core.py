import datetime
import requests
import time

from matplotlib import pyplot
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc
from pylab import *

#from .exceptions import SymbolNotFoundException

# inspired by https://github.com/edgedalmacio/phisix
# which is implented in java
# API_URL = 'http://phisix-api.appspot.com/stocks'
API_URL = 'http://www.pse.com.ph/stockMarket/'


# TODO: move to exceptions.py
class SymbolNotFoundException(Exception):
    pass


class Tsupytero(object):

    def __init__(self):
        pass

    def all(self):
        params = {
            'method': 'getSecuritiesAndIndicesForPublic',
            'ajax': 'true',
        }

        url = '%s%s' % (API_URL, 'home.html')

        req = requests.get(url, params=params)

        ret = None
        if req.status_code == 200:
            ret = req.json()
        return ret


    def find(self, sym):
        params = {
            'method': 'findSecurityOrCompany',
            'ajax': 'true',
            'start': 0,
            'limit': 1,
            'query': sym,
        }

        url = '%s%s' % (API_URL, 'home.html')

        req = requests.get(url, params=params)

        ret = None
        if req.status_code == 200:
            ret = req.json()

        if not ret['count']:
            raise SymbolNotFoundException

        return ret


    def get_latest_data(self, sym):
        data = self.find(sym)

        company_id = data['records'][0]['listedCompany_companyId']
        security_id = data['records'][0]['securityId']

        params = {
            'method': 'fetchHeaderData',
            'ajax': 'true',
            'company': company_id,
            'security': security_id,
        }
        url = '%s%s' % (API_URL, 'companyInfo.html')

        req = requests.post(url, data=params)

        ret = None
        if req.status_code == 200:
            ret = req.json()
        return ret


    def get_recent_data(self, sym):
        data = self.find(sym)

        company_id = data['records'][0]['listedCompany_companyId']
        security_id = data['records'][0]['securityId']

        url = '%s%s' % (API_URL, 'companyInfoHistoricalData.html')
        params = {
            'method': 'getRecentSecurityQuoteData',
            'ajax': 'true',
            'security': security_id,
        }

        req = requests.post(url, data=params)

        ret = None
        if req.status_code == 200:
            ret = req.json()
        return ret

    
    def get_recent_candlestick(self, sym):
        data = self.get_recent_data(sym)

        count = data['count']
        records = data['records']

        prices = []
        for record in reversed(records):
            # convert date string to date then to float
            dt = record['tradingDate'].split(' ')[0]
            dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
            dt = time.mktime(dt.timetuple())
            open_val = float(record['sqOpen'])
            close_val = float(record['sqClose'])
            low_val = float(record['sqLow'])
            high_val = float(record['sqHigh'])
            prices.append((dt, open_val, high_val, low_val, close_val))

        # http://matplotlib.org/examples/pylab_examples/finance_demo.html 
        mondays = WeekdayLocator(MONDAY)
        alldays = DayLocator()
        weekFormatter = DateFormatter('%b %d')
        dayFormatter = DateFormatter('%d')

        fig, ax = pyplot.subplots()
        #fig.subplots_adjust(bottom=0.2)
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
        ax.xaxis.set_major_formatter(weekFormatter)
        ax.xaxis.set_minor_formatter(dayFormatter)
        candlestick_ohlc(ax, prices, width=4, colorup='g')

        ax.xaxis_date()
        ax.autoscale_view()
        pyplot.setp(pyplot.gca().get_xticklabels(), rotation=45, 
                                    horizontalalignment='right')

        pyplot.show()



