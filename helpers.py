###################################################################
#                                                                 #
#           This module consists of helper functions              #
#                                                                 #
###################################################################

import json
import requests
import re
import os

URL = "https://www.alphavantage.co/query"
FUNCTION="TIME_SERIES_DAILY"
INTERVAL="60min"
API_KEY = "7FTMY9P2XGW5PLVF"
INVENTORY_PATH = os.path.join(os.getcwd(), "stocks.json")

requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)

def get_stock_all():
    """
    Return all available stock codes.
    For now it will read codes from stocks.json
    """
    try:
        with open(INVENTORY_PATH) as f:
            data = json.load(f)
            data['count'] = len(data['stocks'])
            return data
    except Exception as ex:
        print(ex)
        return None

def is_valid(args):
    """
    Validate search range filters: values of from and to
    """
    if (len(args) == 2) and ('from' in args) and ('to' in args) and (args['from'] <= args['to']):
        regex_pattern = "2020-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$"
        return re.findall(regex_pattern, args['from']) and re.findall(regex_pattern, args['to'])
    return None


def filter_by_date(data, start, end):
    """
    Return data between start and end dates
    """
    filtered_data = {}
    for key,value in data.items():
        if start <= key <= end:
            filtered_data[key] = value
    return filtered_data

def get_stock_one(stock_code, args=None):
    """
    Get price for give stock code. 
    If data is specified for a given data.
    """
    data = None
    try:
        response = requests.get(url=f"{URL}?function={FUNCTION}&symbol={stock_code}&&apikey={API_KEY}", verify=False)
        if response.status_code == 200:
            data = response.json()["Time Series (Daily)"]
            if args:
                data = filter_by_date(data=data, start=args['from'], end=args['to'])
        else:
            print(response.text)
    except Exception as ex:
        print(ex)
    finally:
        return data