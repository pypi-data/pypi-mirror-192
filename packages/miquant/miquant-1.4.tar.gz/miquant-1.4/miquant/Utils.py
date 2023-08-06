import json
from locale import D_FMT
from requests import get
import pandas as pd
import time

    
class Utils:
    @staticmethod
    def load_basic_info(symbol):
        url = f'https://wichart.vn/wichartapi/wichart/popquick?code={symbol}'
        data = get(url).json()
        return data[0] if data else {}

    @staticmethod
    def load_universe():
        data = get('https://wichart.vn/wichartapi/wichart/danhsachchungkhoan').json()
        columns = ['Ticker', 'Company_name', 'Exchange', 'OutstandingShares', 'Margin', 'Industry_lev3', 'Industry_lev4', 'Listed_date']
        ticker_df = pd.DataFrame(columns=columns)

        # Load Ticker and Company_name from JSON
        ticker_df['Ticker'] = [d['code'] for d in data]
        ticker_df['Company_name'] = [d['fullname_vi'] for d in data]

        # Load remaining data from API for each ticker
        for idx, name in enumerate(ticker_df.index):
            secret_df = Utils.load_basic_info(name)
            if secret_df:
                ticker_df.iloc[idx]['Exchange'] = secret_df['san']
                ticker_df.iloc[idx]['OutstandingShares'] = secret_df['soluongluuhanh']
                ticker_df.iloc[idx]['Margin'] = secret_df['kyquy']
                ticker_df.iloc[idx]['Industry_lev3'] = secret_df['nganhcap3_vi']
                ticker_df.iloc[idx]['Industry_lev4'] = secret_df['nganhcap4_vi']
                ticker_df.iloc[idx]['Listed_date'] = secret_df['ngayniemyet']
        ticker_df.dropna(inplace=True)
        ticker_df.set_index('Ticker', inplace=True)
        return ticker_df