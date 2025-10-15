#Loading and Processing the Kaggle csv File
import pandas as pd

#Loading the Dataset
df = pd.read_csv("data/coin_Bitcoin.csv")

#Converting Date column to datetime format and sorting it
df['Date']=pd.to_datetime(df['Date'])
df=df.sort_values("Date")
df['Source'] = 'Kaggle'


#Fetching Live Price(CoinGecko API)
import requests

def get_Live_Price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    try:
        response=requests.get(url)
        data=response.json()
        return data['bitcoin']['usd']
    
    except:
        return None


#Starting a Streamlit App and Displaying Title and Live Price
import streamlit as st
import matplotlib.pyplot as plt

#Page Configuration
st.set_page_config(page_title="CryptoDash", layout="wide")
st.title("📊 CryptoDash: Bitcoin Price Dashboard")

#Showing Live Price
live_price = get_Live_Price()

if(live_price):
    st.subheader(f"💰 Live Bitcoin Price: **${live_price:,}**")

    #Adding Live Price to Dataset
    import datetime
    today = pd.to_datetime(datetime.date.today())

    #Appending only if it is not in the CSV
    if today > df['Date'].max():
        new_row = pd.DataFrame({'Date': [today], 'Close': [live_price],'Source': ['Live']})
        df = pd.concat([df, new_row], ignore_index=True)
        df = df.sort_values("Date")

else:
    st.warning("⚠️ Could not fetch live price.")


#Adding Date filters in the Sidebar
st.sidebar.header("📅 Filter Date Range")
start_date = st.sidebar.date_input("Start Date", value=df['Date'].min())
end_date = st.sidebar.date_input("End Date", value=df['Date'].max())

#Filtering the Data
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]


#Adding SideBar Toggles
#Showing raw data
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("🧾 Filtered Raw Data")
    st.dataframe(filtered_df)

#Moving Average Checkbox
if st.sidebar.checkbox("Show 30-Day Moving Average"):
    filtered_df['MA30'] = filtered_df['Close'].rolling(window=30).mean()

#Plotting the closing price chart
st.subheader("📈 Bitcoin Closing Price")

kaggle_data = filtered_df[filtered_df['Source'] == 'Kaggle']
live_data = filtered_df[filtered_df['Source'] == 'Live']

#Creating the chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(kaggle_data['Date'], kaggle_data['Close'], label='Kaggle Close Price', color='orange')

if not live_data.empty:
    ax.scatter(live_data['Date'], live_data['Close'], label='Live Price', color='blue', s=100, marker='o')

# If MA30 was added
if 'MA30' in filtered_df.columns:
    ax.plot(filtered_df['Date'], filtered_df['MA30'], label='30-Day MA', color='green')

ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()
ax.grid(True)

#Displaying chart in streamlit
st.pyplot(fig)

#On command prompt: streamlit run streamlit_app.py

























    
