import yfinance as yf
from datetime import date

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.info = self.stock.info
        self.sd = None

    def get_stock_data(self, start_date, end_date):
        """Fetches historical stock data within the specified date range."""
        self.sd = self.stock.history(start=start_date, end=end_date)
        self.sd.columns = self.sd.columns.get_level_values(0)
        self.sd.reset_index(inplace=True)  # Reset the index to make "Date" a regular column
        self.sd['Date'] = self.sd['Date'].dt.date
        self.sd.drop(["Dividends", "Stock Splits"], axis=1, inplace=True, errors='ignore')
        
        return self.sd
    
    def data_to_plot(self, data_type):
        return self.sd[["Date", data_type]]

    def get_stock_info(self):
        """Fetches basic stock information."""
        comp_name = self.info.get("longName", "N/A")
        symbol = self.info.get("symbol", "N/A")
        market_cap = self.info.get("marketCap", "N/A")
        pe_ratio = self.info.get("trailingPE", "N/A")
        open_price = self.sd["Open"][len(self.sd.index) - 1]
        prev_close = self.sd["Close"][len(self.sd.index) - 2]

        return {
            "company_name": comp_name,
            "symbol": symbol,
            "prev_close": prev_close,
            "open_price": open_price,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio
        }
    
    def export_to_csv(self):
        return self.sd.to_csv(f"{self.ticker} - {date.today()}.csv")
    
    def export_to_xlsx(self):
        return self.sd.to_excel(f"{self.ticker} - {date.today()}.xlsx")