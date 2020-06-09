from urllib.parse import urlencode
import json

def call(client, path, params=None):
    url = path + '?' + urlencode(params) if params else path
    response = client.get(url)
    return json.loads(response.data.decode('utf-8'))

def test_index(client):
    result = call(client, '/')
    assert result == "hello"

# def test_plus_one(client):
#     result = call(client, '/plus_one', {'x': 2})
#     assert result['x'] == 3

# def test_minus_one(client):
#     result = call(client, '/minus_one', {'x': 4})
#     assert result['x'] == 3

# def test_pow(client):
#     result = call(client, '/pow', {'x': 4, 'y': 2})
#     assert result['pow(x,y)'] == 16

# def test_square(client):
#     result = call(client, '/square', {'x': 2})
#     assert result['x'] == 4