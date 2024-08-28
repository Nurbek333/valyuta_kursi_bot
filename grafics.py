import matplotlib.pyplot as plt

def plot_historical_prices(prices, symbol):
    dates = [price['time'] for price in prices['Data']['Data']]
    values = [price['close'] for price in prices['Data']['Data']]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o', linestyle='-', color='b')
    plt.title(f'{symbol} Tarixiy Narxlari')
    plt.xlabel('Sana')
    plt.ylabel('Narx (USD)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f'{symbol}_historical_prices.png')
