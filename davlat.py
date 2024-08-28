import requests
import logging

logging.basicConfig(level=logging.INFO)
# API kalitni sozlash
API_KEY = '057fe47cb5e74f51bd2cd600803f865a'

# Valyuta kurslarini olish funksiyasi
def get_currency_rate(fsym, tsym='UZS'):
    url = f'https://api.currencyfreaks.com/latest'
    parameters = {
        'apikey': API_KEY,
        'symbols': tsym  # Qabul qiluvchilar valyutasi
    }
    response = requests.get(url, params=parameters)
    
    if response.status_code != 200:
        return f"Xato: {response.status_code} - {response.text}"
    
    try:
        data = response.json()
        print(f"API Javobi: {data}")  # Javobni konsolga chiqaring
        rates = data.get('rates', {})
        return rates.get(tsym, "Ma'lumot yo'q")
    except requests.exceptions.JSONDecodeError:
        return "JSON formatida javob olinmadi"
