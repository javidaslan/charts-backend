from flask import Flask, request, jsonify
import re

# custom modules
from helpers import *

app = Flask(__name__)



@app.route("/")
def index():
    return "hello"

@app.route("/stocks")
def stocks():
    try:
        stocks = get_stocks()
        return jsonify(stocks)    
    except Exception as ex:
        print(ex)
        return jsonify("Stocks could not be retrieved."), 500

@app.route("/stock/<stock_code>")
def stock(stock_code):
    try:
        args = request.args
        print(args)
        if args:
            if not is_valid(args):
                return jsonify({"error": "Please provide correct range."}), 400
        data = get_stock(stock_code=stock_code, args=args)
        return jsonify({
                    "data": data, 
                    "from": args['from'] if args else None,
                    "to": args['to'] if args else None})            
    except Exception as ex:
        print(ex)
        return jsonify("Stock information could not be retrieved."), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)