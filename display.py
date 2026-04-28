import matplotlib.pyplot as plt
import plotly.express as px

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

#There is no goo sinergy between matplotlib and streamlit, so i would create new graphics for that part. Keeping the old one, being able to used 
#trough the terminal. 

def plot_price_history_streamlit(df, ticker):
    fig = px.line(
        df,
        x=df.index,
        y='Close',
        title=f'Price History {ticker}',
        labels={'Close': 'Price', 'index': 'Date'}
    )
    
    # Añadir MA50
    fig.add_scatter(
        x=df.index,
        y=df['Close'].rolling(50).mean(),
        mode='lines',
        name='MA50',
        line=dict(color='orange')
    )
    
    fig.update_layout(template='plotly_dark')
    return fig


def plot_drawdown_streamlit(drawdown_series, ticker):
    fig = px.area(
        x=drawdown_series.index,
        y=drawdown_series.values,
        title=f'Drawdown History {ticker}',
        labels={'x': 'Date', 'y': 'Drawdown %'}
    )
    
    fig.update_traces(line_color='red', fillcolor='rgba(255,0,0,0.2)')
    fig.update_layout(template='plotly_dark')
    return fig