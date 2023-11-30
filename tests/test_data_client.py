from data_client import YahooFinanceClient

def test_yahoo_finance_client_initialization():
    api = YahooFinanceClient()
    assert isinstance(api, YahooFinanceClient)
