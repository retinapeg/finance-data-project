import yfinance as yf

def download_stock_data(ticker: str):
    data=yf.download(ticker,period='1y',interval = "1d",progress = False)

    return data
