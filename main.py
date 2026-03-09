## ENTRANCE POINT, THE PLACE THAT WE ARE GOING TO RECIEVE THE TICKER´S 
from data import get_stock_data
from metrics import total_return, annualized_volatility, max_drawdown,simplified_sharpe_ratio
from display import plot_price_history


##FIRST OF ALL, we need the name of the ticker to analize. 
stock_name = input("Introduce the name of the active that you would like to "": ")
result = get_stock_data(stock_name.upper())

if result is not None: 
    print(f"--- {stock_name.upper()} Analysis---")
    #Result of first function of rentability
    print(f"Total return: {total_return(result):.2f}%")
    #Result of the annual volatility
    print(f"Annualized volatility: {annualized_volatility(result):.2f}%")
    #Here is the result of the calculacion of the biggest price drop
    print(f"Max Drawdown: {max_drawdown(result):.2f}%")
    print(f"Simplify Sharpe Ratio: {simplified_sharpe_ratio(result):.2f}")
    plot_price_history(result,stock_name.upper())
else: 
    print("----------")
    print("No data found for that ticker.")
    print("----------")

