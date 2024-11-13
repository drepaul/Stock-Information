import streamlit as st
import yfinance as yf
from datetime import datetime
from stock_data import *

st.set_page_config(page_title="Stock Analysis")

# Sidebar for user inputs
st.sidebar.title("Stock Tracker")
ticker_input = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
date_range = st.sidebar.date_input("Select Date Range", [datetime(1980, 6, 1), datetime.today()])
series_type = st.sidebar.selectbox("Series Type", ["Open", "High", "Low", "Close"])
search_button = st.sidebar.button("Search")

# Main Page Layout
stock_info = {"company_name": "", "symbol": "", "prev_close": "", "open_price": "", "market_cap": "", "pe_ratio": ""}
if search_button:
    stock_data = StockData(ticker=ticker_input.upper())
    stock_df = stock_data.get_stock_data(start_date=date_range[0], end_date=date_range[1])
    stock_info.clear()
    stock_info = stock_data.get_stock_info()
    data_to_plot = stock_data.data_to_plot(series_type)

    st.markdown(f"<h1 style='text-align: left;'>{stock_info["company_name"]} ({stock_info["symbol"]})</h1>", unsafe_allow_html=True)

    if stock_data is not None:
        # Line chart for stock price
        st.line_chart(data_to_plot, x="Date", y=series_type, color="#FF0000")
    else:
        st.write("No data found for the specified ticker and date range.")
else:
    st.write("Enter a stock ticker and click Search to see data.")

# Options for analysis methods and actions side by side
st.write("### Analysis Options and Actions")
col0, col1, col2 = st.columns(3)

with col0:
    st.write(f"Previous Close: ${stock_info["prev_close"]}")
    st.write(f"Open: ${stock_info["open_price"]}")
    st.write(f"Market Cap: ${stock_info["market_cap"]}")
    st.write(f"PE Ratio: ${stock_info["pe_ratio"]}")
with col1:
    st.checkbox("Linear Regression")
    st.checkbox("Simple Moving Avg")
    st.checkbox("Neural Network")
    st.checkbox("ARIMA")

with col2:
    st.button("Compare Stock")
    st.button("Download CSV")
    st.button("Download Excel")
