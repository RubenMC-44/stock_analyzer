import matplotlib.pyplot as plt

def plot_price_history (df,ticker):
    plt.plot(df.index,df["Close"],color = "r", label = "Close price")#Historical price line
    
    plt.plot(df.index,df["Close"].rolling(50).mean(),color= "b", label = "MA 50")#Dinamic line #Showing more clearly the trend 
                                                                                #showing the avegare price from the last 50 days
    
    plt.axhline(df["Close"].iloc[0], color = "g", label = "Inicial price" ) #First price horizontal line

    plt.title(f"Historical Price {ticker}")
    plt.xlabel("Date time")
    plt.ylabel("Price")

    plt.legend()
    plt.show() 

def plot_drawdown_series (drawdown_series, ticker):
    plt.figure(figsize=(10, 4))
    plt.plot(drawdown_series.index, drawdown_series, color='r', label='Drawdown')
    plt.fill_between(drawdown_series.index, drawdown_series, 0, alpha=0.3, color='r')
    plt.title(f'Drawdown History {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Drawdown %')
    plt.legend()
    plt.show()