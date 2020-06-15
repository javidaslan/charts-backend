from flask import Flask, request, jsonify
from flask_cors import CORS

# custom modules
from helpers import get_stock_codes, get_monthly_price

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return jsonify("hello")

@app.route("/stocks")
def stocks():
    try:
        stocks = get_stock_codes()
        return jsonify(stocks)    
    except Exception as ex:
        print(ex)
        return jsonify("Stocks could not be retrieved."), 500

@app.route("/stock/<stock_code>")
def stock(stock_code):
    try:
        args = request.args
        if args and 'month' not in args:
            return jsonify({"error": "Please provide correct filter."}), 400
        data = get_monthly_price(stock_code=stock_code.upper(), args=args)
        return jsonify({
            "stock_code": stock_code.upper(),
            "prices": data, 
            "from": args['from'] if args else None,
            "to": args['to'] if args else None})            
    except Exception as ex:
        print(ex)
        return jsonify("Stock information could not be retrieved."), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)