from data_loader import download_stock_data
from analysis import calculate_metrics


def main():
    ticker = "AAPL"
    data = download_stock_data(ticker)
    metrics = calculate_metrics(data)
    print()
    print(f"{ticker} MARKET SUMMARY")
    print("------------------------------")
    print(f"Latest close:           ${metrics['latest_close']:.2f}")
    print(f"Average close:          ${metrics['average_close']:.2f}")
    print(f"Total return:            {metrics['total_return']:.2%}")
    print(f"Annualised volatility:   {metrics['annualised_volatility']:.2%}")
    print(f"Best trading day:        {metrics['best_day']:.2%}")
    print(f"Worst trading day:       {metrics['worst_day']:.2%}")
    print(f"Average daily volume:    {metrics['average_volume']:,.0f}") 
    return data

if __name__ == "__main__":
    main()

