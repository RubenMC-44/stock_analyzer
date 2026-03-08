import matplotlib.pyplot as plt

def plot_price_history (df,ticker):
    plt.plot(df.index,df["Close"],color = "r", label = "Close price")#Historical price line
    plt.plot(df.index,df["Close"].rolling(50).mean(),color= "b", label = "MA 50")#Dinamic line 
    plt.axhline(df["Close"].iloc[0], color = "g", label = "Inicial price" ) #First price horizontal line

    plt.title(f"Historical Price {ticker}")
    plt.xlabel("Date time")
    plt.ylabel("Price")

    plt.legend()
    plt.show() 