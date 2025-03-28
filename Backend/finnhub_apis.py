import finnhub
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("FINNHUB_API_KEY")

# Setup client
finnhub_client = finnhub.Client(api_key=api_key)

def get_company_news(ticker,start_date,end_date):
    try:
        company_news = finnhub_client.company_news(ticker, _from=start_date, to=end_date)
        for news in company_news:
            news["company_name"] = ticker
        
        return company_news
    except Exception as e:
        print(f"Error fetching company news: {e}")
        return []
    
def get_general_news():
    try:
        general_news = finnhub_client.general_news('general', min_id=0)
        return general_news
    except Exception as e:
        print(f"Error fetching general news: {e}")
        return []
    
def get_ohlc_data(ticker, start_date, end_date):
    try:
        ohlc_data = finnhub_client.stock_candles(ticker, 'D', start_date, end_date)
        return ohlc_data
    except Exception as e:
        print(f"Error fetching OHLC data: {e}")
        return {}
    