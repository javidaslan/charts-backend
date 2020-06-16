###################################################################
#                                                                 #
#           This module consists of helper functions              #
#                                                                 #
###################################################################

import json
import requests
import re
import os
from datetime import datetime
from time import strptime
import traceback

URL = "https://www.alphavantage.co/query"
FUNCTION="TIME_SERIES_DAILY"
INTERVAL="60min"
API_KEY = "7FTMY9P2XGW5PLVF"
INVENTORY_PATH = os.path.join(os.getcwd(), "stocks.json")

requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)

def get_stock_codes():
    """
    Return all available stock codes.
    For now it will read codes from stocks.json
    CI Test
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


def filter_by_date(data, month, year):
    """
    Return data between start and end dates
    """
    filtered_data = {}
    for key,value in data.items():
        item_month = key.split('-')[1]
        item_year = year
        if month == item_month and year == item_year:
            filtered_data[key] = value
    return filtered_data

def refine_month(month_name):
    """
    This function refines month name
    """
    try:
        month_number = strptime(month_name[:3],'%b').tm_mon
        return '{:02d}'.format(month_number)
    except Exception:
        print(traceback.format_exc())
    return None


def get_monthly_price(stock_code, args=None):
    """
    Get price for given stock code. 
    If data is specified for a given data.
    """
    data = None
    month = refine_month(args['month'] if args else datetime.now().strftime('%B'))
    year = args['year'] if args else str(datetime.now().year)
    try:
        response = requests.get(url=f"{URL}?function={FUNCTION}&symbol={stock_code}&&apikey={API_KEY}", verify=False)
        if response.status_code == 200:
            data = response.json()["Time Series (Daily)"]
            data = filter_by_date(data=data, month=month, year=year)
        else:
            print(response.text)
            print("response")
    except Exception:
        print(traceback.format_exc())
    finally:
        return data
