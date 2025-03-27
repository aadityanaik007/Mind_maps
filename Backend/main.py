import finnhub
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("FINNHUB_API_KEY")

# Setup client
finnhub_client = finnhub.Client(api_key=api_key)

# Stock candles
res = finnhub_client.quote('AAPL')
print(res)
