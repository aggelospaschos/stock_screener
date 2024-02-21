# Import necessary libraries
from flask import Flask, render_template, request
import yfinance as yf

# Create Flask application instance
app = Flask(__name__)

# Function to fetch current stock data
def fetch_stock_data(symbol):
    try:
        # Create Ticker object for the given stock symbol
        stock = yf.Ticker(symbol)

        # Retrieve basic stock information
        data = stock.info

        # Extract regular market price; if not available, mark as N/A
        if 'regularMarketPrice' in data:
            price = data['regularMarketPrice']
        else:
            price = 'N/A'

        # Construct stock data dictionary
        stock_data = {
            'symbol': data.get('symbol', 'N/A'),
            'longName': data.get('longName', 'N/A'),
            'regularMarketPrice': price,
            'regularMarketVolume': data.get('volume', 'N/A'),
            'marketCap': data.get('marketCap', 'N/A')
        }
        return stock_data
    except Exception as e:

        # Handle exceptions during data fetching
        print("Error fetching stock data:", e)
        return None

# Function to fetch historical stock data
def fetch_historical_data(symbol):
    try:
        # Create Ticker object for the given stock symbol
        stock = yf.Ticker(symbol)

        # Retrieve historical data for the past 1 year
        data = stock.history(period="1y")

        # Format historical data as list of dictionaries containing date and close price
        historical_data = [{'date': str(date), 'close': float(close)} for date, close in zip(data.index, data['Close'])]
        return historical_data
    except Exception as e:

        # Handle exceptions during historical data fetching
        print("Error fetching historical data:", e)
        return None

# Route for home page
@app.route('/')
def home():

    # Render the index.html template
    return render_template('index.html')

# Route for screening stocks
@app.route('/screen', methods=['GET', 'POST'])
def screen_stocks():
    if request.method == 'POST':

        # Extract stock symbol from the form submitted via POST request
        symbol = request.form['symbol']

        # Fetch current stock data for the given symbol
        stock_data = fetch_stock_data(symbol)
        if stock_data:

            # If stock data is successfully fetched, also fetch historical data
            historical_data = fetch_historical_data(symbol)

            # Render the screen.html template with stock data and historical data
            return render_template('screen.html', stock_data=stock_data, historical_data=historical_data)
        else:
            # If stock data fetching failed, render error.html template with appropriate message
            return render_template('error.html', message='Failed to fetch stock data.')
    else:
        # If request method is GET, render the index.html template
        return render_template('index.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)






