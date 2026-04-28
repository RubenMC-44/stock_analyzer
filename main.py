## ENTRANCE POINT, THE PLACE THAT WE ARE GOING TO RECIEVE THE TICKER´S 
from data import get_stock_data
from metrics import total_return, annualized_volatility, max_drawdown, simplified_sharpe_ratio, Drawdown_Series
import pandas as pd 

##FIRST OF ALL, we need the name of the ticker to analize. 
def startAnalysis(stock_names):
    metrics_data_list = []
    for i in stock_names: 
        result = get_stock_data(i.strip().upper())
        if result is not None: 
            metrics_data = {"Name": i.strip().upper(), "Total return": total_return(result), "Annualize volatility": annualized_volatility(result),
                            "Max Drawdown" : max_drawdown(result), "Simplify Sharpe Ratio" : simplified_sharpe_ratio(result) ,"df": result}
            metrics_data_list.append(metrics_data)
        else: 
            print("----------")
            print("No data found for that ticker.")
            print("----------")
    return metrics_data_list
            
def download_newData(metrics_data_list): 
#We give the option, after create the new data, to download it. 
    df_tickers = pd.DataFrame(metrics_data_list)
    df_tickers.to_csv("Data_Tickers.csv", index=False)

if __name__ == "__main__":
    stock_name = input("Introduce the name of the stocks: ")
    stock_names = stock_name.split(",")
    results = startAnalysis(stock_names)
    for ticker_data in results:
        print(ticker_data)
    download_newData(results)
