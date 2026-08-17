from data_loader import download_stock_data


def main():
    data = download_stock_data("AAPL")

    print(data.head())


if __name__ == "__main__":
    main()