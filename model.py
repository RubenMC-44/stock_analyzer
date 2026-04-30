from data import get_stock_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

df = get_stock_data("aapl")

def create_target(df):
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    df.dropna(inplace=True)
    return df

df = create_target(df)

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

df = create_features(df)

features =["MA50", "MA200", "RSI", "Volume"]

X = df[features]
Y = df["Target"]

x_train , x_test, y_train , y_test = train_test_split(X,Y, train_size= 0.80, random_state=42)

#------Random forest RandomForestClassifier-------------
model_forest= RandomForestClassifier(class_weight="balanced")
model_forest.fit(x_train,y_train)

y_pred_forest = model_forest.predict(x_test)
print(classification_report(y_test, y_pred_forest))