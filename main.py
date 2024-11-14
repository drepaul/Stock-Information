import streamlit as st
import yfinance as yf
from datetime import datetime
from stock_data import StockData

# Set Streamlit page configuration
st.set_page_config(page_title="Stock Analysis")

# Sidebar for user inputs
st.sidebar.title("Stock Tracker")
ticker_input = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
date_range = st.sidebar.date_input("Select Date Range", [datetime(1980, 6, 1), datetime.today()])
series_type = st.sidebar.selectbox("Series Type", ["Open", "High", "Low", "Close"])
search_button = st.sidebar.button("Search")
chart_type = st.sidebar.selectbox("Select Chart Type", ["OHLC"])

# Check if data exists in session_state, otherwise initialize it
if 'stock_class' not in st.session_state:
    st.session_state['stock_class'] = None
    st.session_state['stock_data'] = None
    st.session_state['stock_info'] = {
        "company_name": "",
        "symbol": "",
        "prev_close": 0.0,
        "open_price": 0.0,
        "market_cap": 0.0,
        "pe_ratio": 0.0
    }

# Main Page Layout
if search_button:
    # Initialize StockData and store it in session_state
    st.session_state['stock_class'] = StockData(ticker=ticker_input.upper())
    
    # Fetch and store stock data and info
    st.session_state['stock_data'] = st.session_state['stock_class'].get_stock_data(start_date=date_range[0], end_date=date_range[1])
    st.session_state['stock_info'] = st.session_state['stock_class'].get_stock_info()
    st.session_state['data_to_plot'] = st.session_state['stock_class'].data_to_plot(series_type)

# Display Stock Information if it exists in session_state
if st.session_state['stock_class'] is not None:
    stock_info = st.session_state['stock_info']
    stock_data = st.session_state['stock_data']
    data_to_plot = st.session_state['data_to_plot']

    # Display Stock Info Header
    st.markdown(f"<h1 style='text-align: left;'>{stock_info['company_name']} ({stock_info['symbol']})</h1>", unsafe_allow_html=True)

    if stock_data is not None:
        # Line chart for stock price
        st.line_chart(data_to_plot, x="Date", y=series_type)
    else:
        st.write("No data found for the specified ticker and date range.")
else:
    st.write("Enter a stock ticker and click Search to see data.")

# Options for analysis methods and actions side by side
st.write("### Analysis Options and Actions")
col0, col1, col2 = st.columns(3)

with col0:
    st.write(f"Previous Close: ${round(st.session_state['stock_info']['prev_close'], 2)}")
    st.write(f"Open: ${round(st.session_state['stock_info']['open_price'], 2)}")
    st.write(f"Market Cap: ${round(st.session_state['stock_info']['market_cap'], 2)}")
    st.write(f"PE Ratio: ${round(st.session_state['stock_info']['pe_ratio'], 2)}")
with col1:
    st.checkbox("Linear Regression")
    st.checkbox("Multiple Linear Regression")
    st.checkbox("Simple Moving Avg")
    st.checkbox("Neural Network")
    st.checkbox("ARIMA")
with col2:
    st.button("Compare Stock")
    st.button("Download CSV", on_click=lambda: st.session_state['stock_class'].export_to_csv())
    st.button("Download Excel", on_click=lambda: st.session_state['stock_class'].export_to_xlsx())
    