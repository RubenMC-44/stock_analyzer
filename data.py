
import yfinance as yf

## Where we are gonna look for the tickers, and identify the active
def get_stock_data (ticker, period = "1y"): 
    try: 
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

##Check the name introduced, and give the result back
        if df.empty: 
            return None
        else: 
            return df
        
#We use the except, to avoid the crash, show the message instead      
    except Exception as e: 
        print(f"ERROR: Ticker '{ticker}' not found {e}")
        return None
##Check hwo to make it look clean##