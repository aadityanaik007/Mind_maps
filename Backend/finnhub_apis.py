import finnhub
import os
from dotenv import load_dotenv
from datetime import datetime
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("FINNHUB_API_KEY")

# Setup client
finnhub_client = finnhub.Client(api_key=api_key)



def get_company_news(ticker, start_date, end_date):
    try:
        all_news = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        while start <= end:
            chunk_start = start.strftime("%Y-%m-%d")
            chunk_end_date = start + timedelta(days=12)
            chunk_end = min(chunk_end_date, end).strftime("%Y-%m-%d")

            print(f"Fetching news from {chunk_start} to {chunk_end}")

            try:
                chunk_news = finnhub_client.company_news(ticker, _from=chunk_start, to=chunk_end)
            except Exception as e:
                print(f"Error fetching chunk from {chunk_start} to {chunk_end}: {e}")
                chunk_news = []

            if chunk_news:
                print(f"✅ Fetched {len(chunk_news)} articles.")
                for news in chunk_news:
                    try:
                        news["company_name"] = ticker
                        dt = datetime.fromtimestamp(news["datetime"])
                        news["month"] = dt.strftime("%b")
                        news["year"] = dt.strftime("%Y")
                        news["date"] = dt.strftime("%Y-%m-%d")
                        news["day"] = int(dt.strftime("%d"))
                        news.pop("_id", None)
                        news["news_id"] = news["id"]
                        news.pop("id", None)
                        
                        all_news.extend(chunk_news)
                    except Exception as e:
                        print("⚠️ Skipping item with invalid or missing 'datetime'")
            else:
                print("⚠️ No news returned for this chunk.")

            start += timedelta(days=13)

        print(f"🎯 Total news articles collected: {len(all_news)}")
        return all_news

    except Exception as e:
        print(f"❌ Error in company news extraction: {e}")
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

def basic_fundamentals(symbol):
    try:
        data = finnhub_client.company_basic_financials(symbol, 'all')
        return data
    except Exception as e:
        print(f"Error fetching basic fundamentals: {e}")
        return {}