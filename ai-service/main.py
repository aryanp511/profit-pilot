from fastapi import FastAPI
from pydantic import BaseModel
from duckduckgo_search import DDGS
from textblob import TextBlob
import yfinance as yf
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class StockRequest(BaseModel):
    symbol: str

# Helper function to find the real Ticker Symbol
def lookup_ticker(query: str):
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=1&newsCount=0"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        if "quotes" in data and len(data["quotes"]) > 0:
            symbol = data["quotes"][0]["symbol"]
            # Prefer NSE/BSE if available in top result
            if ".NS" in symbol or ".BO" in symbol:
                 return symbol
            # If user typed exact US ticker, return it
            return symbol
            
    except Exception as e:
        logger.error(f"Ticker lookup failed: {e}")
    
    # Fallback: assume user typed correctly or add .NS default
    return query if "." in query else f"{query}.NS"

@app.get("/")
def read_root():
    return {"status": "AI Service is Running"}

# --- NEW ENDPOINT: Get General Market News ---
@app.get("/general-news")
def get_general_news():
    logger.info("Fetching general market news...")
    news_list = []
    try:
        # Search for broad topics
        results = DDGS().news(keywords="top business news india stock market", region="in-en", safesearch="off", max_results=8)
        for article in results:
             news_list.append({
                "headline": article.get('title', 'No Title'),
                "url": article.get('url', '#'),
                "source": article.get('source', 'News'),
                "date": article.get('date', '') # DDGS sometimes provides relative dates
            })
    except Exception as e:
        logger.error(f"Error fetching general news: {e}")
        
    return {"news": news_list}


@app.post("/analyze")
def analyze_stock(request: StockRequest):
    user_input = request.symbol
    logger.info(f"User searched for: {user_input}")

    # STEP 1: Find the Real Ticker
    stock_symbol = lookup_ticker(user_input)
    logger.info(f"Resolved Ticker: {stock_symbol}")

    # --- PART 2: GET FUNDAMENTALS ---
    fundamentals = {}
    try:
        stock = yf.Ticker(stock_symbol)
        # Use fast_info for better performance if available, else fallback to info
        try:
             info = stock.fast_info
             current_price = info.last_price
             market_cap = info.market_cap
             # fast_info doesn't have everything, fetch full info if needed for others
             full_info = stock.info
             pe_ratio = full_info.get("trailingPE", "N/A")
             high_52 = full_info.get("fiftyTwoWeekHigh", "N/A")
             low_52 = full_info.get("fiftyTwoWeekLow", "N/A")
             currency = full_info.get("currency", "INR")
        except:
             # Fallback to slower standard info method
             info = stock.info
             current_price = info.get("currentPrice") or info.get("regularMarketPrice", "N/A")
             market_cap = info.get("marketCap", "N/A")
             pe_ratio = info.get("trailingPE", "N/A")
             high_52 = info.get("fiftyTwoWeekHigh", "N/A")
             low_52 = info.get("fiftyTwoWeekLow", "N/A")
             currency = info.get("currency", "INR")
        
        fundamentals = {
            "current_price": current_price,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "high_52": high_52,
            "low_52": low_52,
            "currency": currency
        }
    except Exception as e:
        logger.error(f"Error fetching fundamentals: {str(e)}")
        fundamentals = {"error": "Could not fetch data"}

    # --- PART 3: GET NEWS ---
    news_summary = []
    total_sentiment = 0

    try:
        search_query = f"{stock_symbol} stock news"
        results = DDGS().news(keywords=search_query, region="in-en", safesearch="off", max_results=5)
        
        for article in results:
            title = article.get('title', 'No Title')
            link = article.get('url', '#')
            
            blob = TextBlob(title)
            sentiment_score = blob.sentiment.polarity
            total_sentiment += sentiment_score
            
            news_summary.append({
                "headline": title,
                "score": round(sentiment_score, 2),
                "url": link
            })

    except Exception as e:
        logger.error(f"Error fetching news: {e}")

    # --- PART 4: VERDICT ---
    count = len(news_summary)
    avg_score = total_sentiment / count if count > 0 else 0
    
    verdict = "NEUTRAL"
    if avg_score > 0.05:
        verdict = "POSITIVE (Bullish)"
    elif avg_score < -0.05:
        verdict = "NEGATIVE (Bearish)"

    return {
        "stock": stock_symbol,
        "verdict": verdict,
        "average_sentiment_score": round(avg_score, 2),
        "fundamentals": fundamentals,
        "news_analysis": news_summary
    }