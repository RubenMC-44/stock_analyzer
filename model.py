from data import get_stock_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def create_target(df):
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df.dropna(inplace=True)
    return df

def create_features(df): 
    # Moving averages to identify trend direction
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()
    
    # RSI calculation (14-day window)
    delta = df["Close"].diff()          # Daily price change
    gain = delta.clip(lower=0)          # Keep only positive changes (gains)
    loss = -delta.clip(upper=0)         # Keep only negative changes (losses, made positive)
    avg_gain = gain.rolling(14).mean()  # Average gain over 14 days
    avg_loss = loss.rolling(14).mean()  # Average loss over 14 days
    rs = avg_gain / avg_loss            # Relative strength
    df["RSI"] = 100 - (100 / (1 + rs)) # RSI formula
    
    # Drop rows with NaN values (caused by rolling windows)
    df.dropna(inplace=True)
    return df

def train_model(df): 
    features =["MA50", "MA200", "RSI", "Volume"]
    X = df[features]
    Y = df["Target"]
    x_train , x_test, y_train , y_test = train_test_split(X,Y, train_size= 0.8, random_state=42)
    #------Random forest RandomForestClassifier-------------
    model= RandomForestClassifier(class_weight="balanced")
    model.fit(x_train,y_train)
    y_pred_forest = model.predict(x_test)
    signals = model.predict(X) #Creating signs with the whole target. In this case X
    classification_report(y_test, y_pred_forest)
    return model,signals, classification_report(y_test, y_pred_forest)

def backtesting(df): 
    df["Daily_return"] = df["Close"].pct_change()
    df["Strategy_return"]= df["Daily_return"] * df["Signal"] # Combine the columns to know which signal works
    df["Strategy_capital"] = 1000 * (1 + df["Strategy_return"]).cumprod() #This collumnd will follow the simplicity. First day you buy and you hold till last day.
    df["BuyHold_capital"] = 1000 * (1 + df["Daily_return"]).cumprod() #More "complicate" stragety, will sell and buy following the signals, so will change everyday.
    return df

#The trys always need to come whit a if name, then we can check if all is working as expected
if __name__ == "__main__":
    stock_name = input("Introduce the name of the stocks: ")
    df = stock_name
    df = get_stock_data(df)
    df = create_target(df)
    df = create_features(df)
    model, signals, report = train_model(df)
    df["Signal"] = signals
    df = backtesting(df)
    print(df[["Close", "Signal", "Daily_return","Strategy_return","Strategy_capital","BuyHold_capital"]].head(10))
    print(report)