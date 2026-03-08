##Financial calculations: Financial Calculations: Total period return, annualized volatility,
# historical maximum/minimum, and simplified Sharpe ratio

import pandas
import numpy as np 


#We calculate the total return for every ticker.
def total_return (df): 
    """
    Calculates the total percentage return of the asset over the entire period.
    Formula: ((Last Price - First Price) / First Price) * 100
    """
    return((df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]) * 100 

def annualized_volatility (df): 
    """
    Calculates the annualized volatility based on daily price changes.
    We assume 252 trading days in a year.
    """
    #We calculate daily porcentage returns
    daily_returns = df["Close"].pct_change() 
    #Standart desviation for the daily returns
    std = np.std(daily_returns) 
    # Annualize the standard deviation: (Daily Std * Square Root of 252)
    return ((std * np.sqrt(252)) *100) 

def max_drawdown (df): 
    """
    Calculates the Maximum Drawdown (MDD), which measures the largest 
    peak-to-trough decline in the asset's value.
    """
    # Identify the running maximum price up to each point in time
    rolling_max = df["Close"].cummax()
    # Calculate the percentage drop from that peak
    drawdown = ((df["Close"]- rolling_max ) / rolling_max) * 100 
    # Return the lowest (most negative) value found
    return drawdown.min() 

def simplified_sharpe_ratio (df): 
    ''' The Sharpe Ratio measures the excess return per unit of risk.
    A higher Sharpe Ratio indicates that the asset provides better 
    risk-adjusted returns without taking on excessive volatility'''
    return ((total_return(df) *0.01) / (annualized_volatility(df)*0.01)) #It must be on the same scale, not on porcentage, this is whhy we multiply for 0.01

    



