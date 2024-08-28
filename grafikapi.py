import requests
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = 'e60f1dfbf1e1110fd527af5b91f1e97a79cff8bfa7686bf61d126c7a69c29580'

def get_historical_prices(symbol, currency='USD', limit=30):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    parameters = {
        'fsym': symbol,
        'tsym': currency,
        'limit': limit
    }
    headers = {
        'authorization': f'Apikey {API_KEY}'
    }
    response = requests.get(url, headers=headers, params=parameters)
    return response.json()

def plot_historical_prices(prices, symbol):
    data = prices['Data']['Data']
    dates = [datetime.fromtimestamp(price['time']) for price in data]
    values = [price['close'] for price in data]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o', linestyle='-', color='b')
    plt.title(f'{symbol} Tarixiy Narxlari')
    plt.xlabel('Sana')
    plt.ylabel('Narx (USD)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.show()  # Grafikni ekranga chiqarish
