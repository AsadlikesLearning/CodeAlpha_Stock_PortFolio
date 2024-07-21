import os
from flask import Flask, render_template, request, redirect, url_for, flash
import finnhub
import requests
from functools import lru_cache

app = Flask(__name__)
app.secret_key = 'Asad'  # Replace with a real secret key
API_KEY = 'cqegu9pr01qm14qaf0ngcqegu9pr01qm14qaf0o0'  # Replace with your actual Finnhub API key
LOGO_API_URL = 'https://logo.clearbit.com/'

# Finnhub client setup
finnhub_client = finnhub.Client(api_key=API_KEY)

portfolio = []


def validate_symbol(symbol):
    try:
        result = finnhub_client.symbol_lookup(symbol)

        # Print the data for debugging purposes
        print(f"Validation response data for {symbol}: {result}")

        if result['count'] > 0:
            return True
        else:
            flash(f"Invalid symbol '{symbol}'. Please check and try again.", "error")
            return False
    except Exception as e:
        flash(f"Error validating symbol '{symbol}': {str(e)}", "error")
        return False


@app.route('/')
def index():
    return render_template('index.html', portfolio=portfolio)


@app.route('/add', methods=['POST'])
def add_stock():
    symbol = request.form.get('symbol').upper()
    if symbol:
        if validate_symbol(symbol):
            stock_data = get_stock_data(symbol)
            if stock_data:
                portfolio.append(stock_data)
                flash(f"Stock {symbol} added successfully!", "success")
            else:
                flash(f"Unable to add stock '{symbol}'. Please try again later.", "error")
    return redirect(url_for('index'))


@app.route('/remove/<symbol>')
def remove_stock(symbol):
    global portfolio
    portfolio = [stock for stock in portfolio if stock['symbol'] != symbol]
    flash(f"Stock {symbol} removed from portfolio.", "success")
    return redirect(url_for('index'))


def get_stock_data(symbol):
    try:
        stock_quote = finnhub_client.quote(symbol)
        stock_profile = finnhub_client.company_profile2(symbol=symbol)

        # Print the data for debugging purposes
        print(f"Stock quote for {symbol}: {stock_quote}")
        print(f"Stock profile for {symbol}: {stock_profile}")

        if stock_quote and stock_profile:
            stock_info = {
                'symbol': symbol,
                'price': stock_quote['c'],
                'timestamp': stock_quote['t'],
                'logo_url': get_logo_url(symbol)
            }
            return stock_info
        else:
            flash(f"Invalid data received for symbol '{symbol}'. Please check the symbol and try again.", "error")
            return None
    except Exception as e:
        flash(f"Error fetching data for '{symbol}': {str(e)}", "error")
        return None


@lru_cache(maxsize=100)
def get_logo_url(symbol):
    url = f"{LOGO_API_URL}{symbol.lower()}.com"
    try:
        response = requests.head(url, timeout=2)
        if response.status_code == 200:
            return url
    except requests.RequestException:
        pass
    return url_for('static', filename='default_logo.png')


if __name__ == '__main__':
    app.run(debug=True)
