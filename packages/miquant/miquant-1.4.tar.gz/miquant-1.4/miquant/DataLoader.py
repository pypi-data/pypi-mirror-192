import json
from locale import D_FMT
from requests import get
import pandas as pd
import time

class DataLoader:
    @staticmethod
    def load_stock_data(symbol, start, end):
        '''
        Returns: stock OHLCV dataframe
        '''
        baseLoader = BaseLoader()
        data = baseLoader.get_data(symbol=symbol, type='stock', resolution='D', start=start, end=end)
        df = pd.DataFrame.from_dict(data['data'])
        df.set_index('tradingDate', inplace=True)
        df.index = pd.to_datetime(df.index)
        df.index = df.index.strftime('%Y-%m-%d')
        if df.index[-1] == df.index[-2]:
            df.drop(df.index[-1], inplace=True)
        return df

    @staticmethod
    def load_index_data(symbol, start, end):
        '''
        Returns: index OHLCV dataframe
        '''
        baseLoader = BaseLoader()
        data = baseLoader.get_data(symbol=symbol, type='index', resolution='D', start=start, end=end)
        df = pd.DataFrame.from_dict(data['data'])
        df.set_index('tradingDate', inplace=True)
        df.index = pd.to_datetime(df.index)
        df.index = df.index.strftime('%Y-%m-%d')
        df = df[:end]
        return df
    
class BaseLoader:
    def __init__(self):
        pass

    def get_data(self, symbol, type, resolution, start, end):
        timeFormat = '%Y-%m-%d'
        startDate = str(int(time.mktime(time.strptime(start, timeFormat))))
        endDate = str(int(time.mktime(time.strptime(end, timeFormat))))
        API_LOAD = f"https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/bars-long-term?ticker={symbol}&type={type}&resolution={resolution}&from={startDate}&to={endDate}"
        data = json.loads(get(API_LOAD).text)
        return data