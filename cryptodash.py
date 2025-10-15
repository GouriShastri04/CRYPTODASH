#CryptoDash

import pandas as pd
import matplotlib.pyplot as plt

#Load the Bitcoin data
df=pd.read_csv("data/coin_Bitcoin.csv")

#Convert timestamp column to datetime
df['Date']=pd.to_datetime(df['Date'])

#Sort by date (Oldest to Latest)
df=df.sort_values('Date')

#Plot closing prices over time
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Close'], label='BTC Close Price', color='orange')
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
