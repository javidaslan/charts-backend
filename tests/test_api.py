from urllib.parse import urlencode
import json
import pytest


def call(client, path, params=None):
    url = path + '?' + urlencode(params) if params else path
    response = client.get(url)
    return json.loads(response.data.decode('utf-8'))

def test_index(client):
    result = call(client, '/')
    assert result == "hello"

def test_stocks(client):
    result = call(client, '/stocks')
    keys = ['stocks', 'count']
    assert all([key in result for key in keys])

@pytest.mark.filterwarnings('ignore::urllib3.exceptions.InsecureRequestWarning')
def test_stock(client):
    result = call(client, '/stock/AAPL')
    keys = ['stock_code', 'prices', 'year', 'month']
    assert all([key in result for key in keys])