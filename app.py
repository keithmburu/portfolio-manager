from dateutil import parser as dateparser
from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api, reqparse
import mysql.connector
from flask_cors import CORS 
from datetime import datetime, timedelta
import yfinance as yf

app = Flask(__name__)
api = Api(app)
CORS(app)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="training",
        password="1234567A",
        database="TAPHK"
    )

class HomeResource(Resource):
    def get(self):
        return send_from_directory('static', 'index.html')
    
class PortfolioResource(Resource):
    def get(self):
        with get_db() as db, db.cursor() as cursor:
            # Retrieve stocks with positive amount holding
            cursor.execute('''SELECT * FROM portfolio WHERE amount_holding > 0''')
            portfolio = cursor.fetchall()
            profit = {}
            # Calculate profit for each stock
            for stock in portfolio:
                # Retrieve the latest close price for the stock
                cursor.execute('''SELECT close_price FROM stock_data WHERE portfolio_id = %s ORDER BY date DESC LIMIT 1''', (stock[0],))
                latest_price_result = cursor.fetchone()[0]
                # calculate the profit for the stock based on the latest close price and the amount_holding
                profit[stock[2]] = float(latest_price_result)*stock[3] - float(stock[6])
                
            
            cursor.execute('''SELECT * FROM historical_networth''')
            networth = cursor.fetchall()
            cursor.close()
        
        return jsonify({"portfolio": portfolio, "networth": networth, "profit": profit})


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("stock_ticker", required=True)
        parser.add_argument("stock_name", required=True)
        parser.add_argument("amount_holding", required=True, type=int)
        parser.add_argument("buy_datetime", required=True)
        args = parser.parse_args()

        stock_ticker = args["stock_ticker"]
        stock_name = args["stock_name"]
        amount_holding = args["amount_holding"]

        
        try:
            # Parse start_datetime using dateutil.parser
            buy_datetime = dateparser.parse(args["buy_datetime"])
            buy_datetime = buy_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        except Exception as e:
            return {"error": "Invalid buy_datetime format"}, 400

        # fetch the latest close price for the asset with yahoo api
        stock = yf.Ticker(stock_ticker)
        yahoo_buy_date = buy_datetime.strftime('%Y-%m-%d')
        next_date = buy_datetime + timedelta(days=1)
        yahoo_next_date = next_date.strftime('%Y-%m-%d')
        historical_data = stock.history(start=yahoo_buy_date, end=yahoo_next_date)
        
        # Check if data is available for the target date
        if not historical_data.empty:
            closing_price = float(historical_data['Close'].values[0])
            high_price = float(historical_data['High'].values[0])
            low_price = float(historical_data['Low'].values[0])
            open_price = float(historical_data['Open'].values[0])
        else:
            return ({"error": "No data available for the given stock"}, 400)
        
        cost = amount_holding * closing_price
        
        # flag for re-adding existing stocks
        reAdd = False
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT COUNT(*) FROM portfolio WHERE stock_ticker = %s;''', (stock_ticker,))
            count = cursor.fetchone()[0]
            if count and count > 0:
                cursor.execute('''SELECT amount_holding FROM portfolio WHERE stock_ticker = %s;''', (stock_ticker,))
                amount = cursor.fetchone()[0]
                if amount != 0:
                    return ({"error": f"Stock already exists, amount holding {amount}"}, 400)
                else:
                    reAdd = True
            
            # get the current networth for the portfolio
            cursor.execute('''SELECT networth FROM historical_networth WHERE date = %s''', (buy_datetime,))
            networth = cursor.fetchone()[0]
            updated_networth = networth + cost
            if reAdd:
                # Fetch the portfolio_id before updating
                cursor.execute('''SELECT id FROM portfolio WHERE stock_ticker = %s;''', (stock_ticker,))
                portfolio_id = cursor.fetchone()[0]
                
                cursor.execute('''UPDATE portfolio 
                  SET amount_holding = %s, buy_datetime = %s, cost = %s
                  WHERE stock_ticker = %s''',
               (amount_holding, buy_datetime, cost, stock_ticker))
                db.commit()
            else:    
                cursor.execute('''INSERT INTO portfolio 
                            (stock_ticker, stock_name, amount_holding, buy_datetime, cost)
                            VALUES (%s, %s, %s, %s, %s)''',
                            (stock_ticker, stock_name, amount_holding, buy_datetime, cost))

                # Retrieve the last inserted row's ID
                portfolio_id = cursor.lastrowid
                db.commit()
                
            # create fake data for inserting into the stock_data table
            cursor.execute('''INSERT INTO  stock_data 
                        (stock_ticker, stock_name, close_price, high_price, low_price, open_price,portfolio_id,date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                        (stock_ticker, stock_name, closing_price, high_price, low_price, open_price,portfolio_id,buy_datetime))
            db.commit()
            
            # Insert the transaction into the stock_transactions table
            cursor.execute('''INSERT INTO stock_transactions 
                              (stock_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (portfolio_id, 'BUY', buy_datetime, amount_holding, closing_price))

            db.commit()

            cursor.execute('''UPDATE historical_networth SET networth=%s WHERE date=%s''',
                           (updated_networth, buy_datetime))
            db.commit()
            cursor.close()
            
        resource_url = api.url_for(AssetResource, portfolio_id=portfolio_id, _external=True)
        insert_ok = ({"message": "Added new stock to portfolio"}, 201, {"Location": f"{resource_url}"})
        insert_failed = ({"error": "Failed to add new stock to portfolio"}, 400)
        return insert_ok if cursor.rowcount else insert_failed

class AssetResource(Resource):
    def get(self, portfolio_id):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM stock_data WHERE portfolio_id = %s''', (portfolio_id,))
            stock = cursor.fetchall()
            cursor.execute('''SELECT * FROM stock_transactions WHERE stock_id = %s''', (portfolio_id,))
            transactions = cursor.fetchall()
            cursor.execute('''SELECT * FROM portfolio WHERE id = %s''', (portfolio_id,))
            portfolio = cursor.fetchone()
            cursor.execute('''SELECT close_price FROM stock_data WHERE portfolio_id = %s ORDER BY DATEDIFF(date, %s) ASC LIMIT 1''', (portfolio_id, datetime.now()))
            nearest_price = cursor.fetchall()
            nearest_price = nearest_price[0][0]
            cursor.close()
            

        return jsonify({"portfolio":portfolio, "stocks":stock,"transactions": transactions,"nearest_price":nearest_price})

    # put with the assumption
    def put(self, portfolio_id):
        parser = reqparse.RequestParser()
        parser.add_argument("transaction_type", required=True, choices=["BUY", "SELL"])
        parser.add_argument("transaction_amount", required=True, type=int)
        parser.add_argument("transaction_price", required=True, type=float)
        parser.add_argument("transaction_datetime", required=True)
        args = parser.parse_args()

        transaction_type = args["transaction_type"]
        transaction_amount = args["transaction_amount"]
        
        try:
            transaction_datetime = dateparser.parse(args["transaction_datetime"])
            transaction_datetime = transaction_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        except Exception as e:
            return {"error": "Invalid transaction_datetime format"}, 400

        with get_db() as db, db.cursor() as cursor:
            # Retrieve the current amount holding for the stock
            cursor.execute('''SELECT amount_holding,cost FROM portfolio WHERE id = %s''', (portfolio_id,))
            current_amount_holding,cost = cursor.fetchone()
            
            # get the current price for the stock
            cursor.execute('''SELECT close_price FROM stock_data WHERE portfolio_id = %s AND date = %s''', (portfolio_id,transaction_datetime,))
            action_price = cursor.fetchone()[0]
            
            # get the current networth for the portfolio
            cursor.execute('''SELECT networth FROM historical_networth WHERE date = %s''', (transaction_datetime,))
            networth = cursor.fetchone()[0]
            
            if transaction_type == "BUY":
                # Calculate and update new amount holding
                updated_amount_holding = current_amount_holding + transaction_amount
                updated_cost = cost + transaction_amount * action_price
                updated_networth = networth + transaction_amount * action_price
            elif transaction_type == "SELL":
                if transaction_amount > current_amount_holding:
                    return {"error": "Not enough stocks to sell"}, 400
                else:
                    # Calculate and update new amount holding
                    updated_amount_holding = current_amount_holding - transaction_amount
                    if updated_amount_holding == 0:
                        updated_cost = 0
                    else:
                        updated_cost = cost - transaction_amount * action_price
                    updated_networth = networth - transaction_amount * action_price

            # Insert the transaction into the stock_transactions table
            cursor.execute('''INSERT INTO stock_transactions 
                              (stock_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (portfolio_id, transaction_type, transaction_datetime, transaction_amount, action_price))
            db.commit()

            # Update the portfolio's amount_holding after transaction
            cursor.execute('''UPDATE portfolio SET amount_holding=%s, cost=%s WHERE id=%s''',
                           (updated_amount_holding,updated_cost, portfolio_id))
            db.commit()
            
            cursor.execute('''UPDATE historical_networth SET networth=%s WHERE date=%s''',
                           (updated_networth, transaction_datetime))
            db.commit()
            
            cursor.close()
                           

            # Return a response indicating success
            return {"message": f"{transaction_type} transaction completed successfully, current amount holding:{updated_amount_holding}"}, 200

    
# remove the delete function since we cannot delete a portfolio item
# since its id is using as a foreign key in the stock_data table
# if sell all the shares of the stock, just set the amount_holding to 0
	
    # # delete the stock from the portfolio (i.e. sell all of it)    
    # def delete(self, portfolio_id,transaction_datetime):
    #     with get_db() as db, db.cursor() as cursor:
    #         # get current amount_holding
    #         cursor.execute('''SELECT amount_holding FROM portfolio WHERE id = %s''', (portfolio_id,))
    #         current_amount_holding = cursor.fetchone()[0]
            
    #         # get the latest closing price
    #         cursor.execute('''SELECT close_price
    #                           FROM stock_data
    #                           WHERE portfolio_id = %s
    #                           ORDER BY date DESC
    #                           LIMIT 1''', (portfolio_id,))
    #         transaction_price = cursor.fetchone()[0]
        
    #         # Insert the transaction into the stock_transactions table
    #         cursor.execute('''INSERT INTO stock_transactions 
    #                           (stock_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
    #                           VALUES (%s, %s, %s, %s, %s)''',
    #                        (portfolio_id, "SELL", transaction_datetime, current_amount_holding, transaction_price))
    #         db.commit()
    #         cursor.execute('''DELETE FROM portfolio WHERE id = %s''', (portfolio_id,))
            
    #         db.commit()
    #     return {"message": "Removed stock from portfolio"}, 200


 
api.add_resource(HomeResource, '/')   
api.add_resource(PortfolioResource, '/portfolio')
# api.add_resource(StocksResource, '/stocks')
# api.add_resource(BondsResource, '/bonds')
# api.add_resource(CashResource, '/cash')
api.add_resource(AssetResource, '/portfolio/<int:portfolio_id>')


if __name__ == '__main__':
    app.run()
