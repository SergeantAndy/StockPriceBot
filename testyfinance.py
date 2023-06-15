import yfinance as yf

def test_yfinance_download():
    symbol = 'AAPL'
    data = yf.download(symbol)
    assert data is not None
    print("Тест yfinance.download() пройдено успішно")

def test_yfinance_ticker_info():
    symbol = 'AAPL'
    required_fields = ['longName', 'sector', 'country']
    info = yf.Ticker(symbol).info
    assert all(field in info for field in required_fields)
    print("Тест yfinance.Ticker.info пройдено успішно")

def test_yfinance_tickers():
    symbols = ['AAPL', 'GOOGL', 'MSFT']
    tickers = yf.Tickers(symbols)
    info = tickers.tickers
    required_fields = ['longName', 'sector', 'country']
    assert all(field in info[symbol].info for symbol in symbols for field in required_fields)
    print("Тест yfinance.Tickers пройдено успішно")

def test_yfinance_financials():
    symbol = 'AAPL'
    retry_limit = 3  # Максимальна кількість спроб
    retry_count = 0  # Лічильник спроб

    while retry_count < retry_limit:
        try:
            financials = yf.Ticker(symbol).financials
            required_columns = ['Revenue', 'Net Income', 'Total Assets']
            assert not financials.empty and all(column in financials.columns for column in required_columns)
            print("Тест yfinance.Ticker.financials пройдено успішно")
            return  # Вихід з циклу у разі успішного проходження тесту
        except Exception as e:
            retry_count += 1
            print(f"Помилка у виконанні запиту ({retry_count}/{retry_limit}): {e}")

    print("Не вдалося пройти тест yfinance.Ticker.financials")

def test_yfinance_holders():
    symbol = 'AAPL'

    try:
        holders = yf.Ticker(symbol).get_major_holders()
        required_fields = ['Date Reported', 'Holder', 'Shares', 'Value']
        assert holders is not None and all(field in holders.columns for field in required_fields)
        print("Тест yfinance.Ticker.get_major_holders пройдено успішно")
    except Exception as e:
        print(f"Не вдалося пройти тест yfinance.Ticker.get_major_holders: {e}")



# Виклик тестів
test_yfinance_download()
test_yfinance_ticker_info()
test_yfinance_tickers()
test_yfinance_financials()
test_yfinance_holders()
