import pandas as pd
import numpy as np
import requests

import requests

API_KEY = 'BMUG2ALOVF846DVB'
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data['Time Series (1min)']
