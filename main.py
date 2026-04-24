## ENTRANCE POINT, THE PLACE THAT WE ARE GOING TO RECIEVE THE TICKER´S 
from data import get_stock_data
from metrics import total_return, annualized_volatility, max_drawdown, simplified_sharpe_ratio, Drawdown_Series
from display import plot_price_history, plot_drawdown_series
import pandas as pd 


##FIRST OF ALL, we need the name of the ticker to analize. 
metrics_data_list = []
stock_name = input("Introduce the name of the active that you would like to analyze: ")
stock_names = stock_name.split(",")
for i in stock_names: 
    result = get_stock_data(i.strip().upper())
    if result is not None: 
        print(f"--- {i.strip().upper()} Analysis---")
        #Result of first function of rentability
        print(f"Total return: {total_return(result):.2f}%")
        #Result of the annual volatility
        print(f"Annualized volatility: {annualized_volatility(result):.2f}%")
        #Here is the result of the calculacion of the biggest price drop
        print(f"Max Drawdown: {max_drawdown(result):.2f}%")
        print(f"Simplify Sharpe Ratio: {simplified_sharpe_ratio(result):.2f}")
        plot_price_history(result,i.strip().upper())
        drawdown_series = Drawdown_Series(result)
        plot_drawdown_series(drawdown_series, i.strip().upper())
        metrics_data = {"Name": i.strip().upper(), "Total return": total_return(result), "Annualize volatility": annualized_volatility(result),
                        "Max Drawdown" : max_drawdown(result), "Simplify Sharpe Ratio" : simplified_sharpe_ratio(result)}
        metrics_data_list.append(metrics_data)
    else: 
        print("----------")
        print("No data found for that ticker.")
        print("----------")

df_tickers = pd.DataFrame(metrics_data_list)
df_tickers.to_csv("Data_Tickers.csv", index=False)