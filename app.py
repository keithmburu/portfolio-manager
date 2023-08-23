import random
from dateutil import parser as dateparser
from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api, reqparse
import mysql.connector
from flask_cors import CORS 
from datetime import datetime
from datetime import datetime

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
            # Retrieve assets with positive amount holding
            cursor.execute('''SELECT * FROM portfolio WHERE amount_holding > 0''')
            portfolio = cursor.fetchall()
            profit = {}
            # Calculate profit for each asset
            for asset in portfolio:
                # Retrieve the latest close price for the asset
                cursor.execute('''SELECT close_price FROM asset_data WHERE portfolio_id = %s ORDER BY date DESC LIMIT 1''', (asset[0],))
                latest_price_result = cursor.fetchone()[0]
                # calculate the profit for the asset based on the latest close price and the amount_holding
                profit[asset[3]] = float(latest_price_result)*asset[4] - float(asset[9])
                
            
            cursor.execute('''SELECT * FROM historical_networth''')
            networth = cursor.fetchall()
        
        return jsonify({"portfolio": portfolio, "networth": networth, "profit": profit})


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type", required=True)
        parser.add_argument("asset_ticker")
        parser.add_argument("asset_name", required=True)
        parser.add_argument("amount_holding", required=True, type=int)
        parser.add_argument("buy_datetime", required=True)
        parser.add_argument("mature_datetime")
        parser.add_argument("currency")
        args = parser.parse_args()

        asset_type = args["asset_type"]
        asset_ticker = args["asset_ticker"]
        asset_name = args["asset_name"]
        amount_holding = args["amount_holding"]

        try:
            # Parse start_datetime using dateutil.parser
            buy_datetime = dateparser.parse(args["buy_datetime"])
            buy_datetime = buy_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        except Exception as e:
            return {"error": "Invalid buy_datetime format"}, 400

        if args["mature_datetime"]:
            try:
                # Parse mature_datetime using dateutil.parser
                mature_datetime = dateparser.parse(args["mature_datetime"])
                mature_datetime = mature_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            except Exception as e:
                return {"error": "Invalid mature_datetime format"}, 400
        else:
            mature_datetime = None

        currency = args["currency"].upper() if args["currency"] else None
        # get the current networth for the portfolio
        cursor.execute('''SELECT networth FROM historical_networth WHERE date = %s''', (buy_datetime,))
        networth = cursor.fetchone()[0]

        # randomly generate some price for inserting into tables
        closing_price = round(random.uniform(10, 100), 2)
        high_price = round(closing_price * random.uniform(1.01, 1.1), 2)
        low_price = round(closing_price * random.uniform(0.9, 0.99), 2)
        open_price = round(random.uniform(low_price, high_price), 2)
        
        cost = amount_holding * closing_price
        
        updated_networth = networth + cost
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''INSERT INTO portfolio 
                          (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, cost)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                           (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency, cost))

            # Retrieve the last inserted row's ID
            portfolio_id = cursor.lastrowid
            db.commit()
            
            # create fake data for inserting into the asset_data table
            cursor.execute('''INSERT INTO  asset_data 
                           (asset_type, asset_ticker, asset_name, close_price, high_price, low_price, open_price,portfolio_id,date)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                           (asset_type, asset_ticker, asset_name, closing_price, high_price, low_price, open_price,portfolio_id,buy_datetime))
            
            
            # Insert the transaction into the asset_transactions table
            cursor.execute('''INSERT INTO asset_transactions 
                              (asset_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (portfolio_id, 'BUY', buy_datetime, amount_holding, closing_price))

            db.commit()

            cursor.execute('''UPDATE historical_networth SET networth=%s WHERE date=%s''',
                           (updated_networth, buy_datetime))
            db.commit()
        resource_url = api.url_for(AssetResource, portfolio_id=portfolio_id, _external=True)
        insert_ok = ({"message": "Added new asset to portfolio"}, 201, {"Location": f"{resource_url}"})
        insert_failed = ({"error": "Failed to add new asset to portfolio"}, 400)
        return insert_ok if cursor.rowcount else insert_failed



# class StocksResource(Resource):
#     def get(self):
#         with get_db() as db, db.cursor() as cursor:
#             cursor.execute('''SELECT * FROM portfolio WHERE asset_type = stock''')
#             stocks = cursor.fetchall()
#         return jsonify(stocks)


# class BondsResource(Resource):
#     def get(self):
#         with get_db() as db, db.cursor() as cursor:
#             cursor.execute('''SELECT * FROM portfolio WHERE asset_type = bond''')
#             bonds = cursor.fetchall()
#         return jsonify(bonds)


# class CashResource(Resource):
#     def get(self):
#         with get_db() as db, db.cursor() as cursor:
#             cursor.execute('''SELECT * FROM portfolio WHERE asset_type = cash''')
#             cash = cursor.fetchall()
#         return jsonify(cash)


class AssetResource(Resource):
    def get(self, portfolio_id):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM asset_data WHERE portfolio_id = %s''', (portfolio_id,))
            asset = cursor.fetchall()
            cursor.execute('''SELECT * FROM asset_transactions WHERE asset_id = %s''', (portfolio_id,))
            transactions = cursor.fetchall()
            cursor.execute('''SELECT * FROM portfolio WHERE id = %s''', (portfolio_id,))
            portfolio = cursor.fetchone()
            cursor.execute('''SELECT close_price FROM asset_data WHERE portfolio_id = %s ORDER BY DATEDIFF(date, %s) ASC LIMIT 1''', (portfolio_id, datetime.now()))
            nearest_price = cursor.fetchone()[0]

        return jsonify({"portfolio":portfolio, "assets":asset,"transactions": transactions,"nearest_price":nearest_price})

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
            # Retrieve the current amount holding for the asset
            cursor.execute('''SELECT amount_holding,cost FROM portfolio WHERE id = %s''', (portfolio_id,))
            current_amount_holding,cost = cursor.fetchone()
            
            # get the current price for the asset
            cursor.execute('''SELECT close_price FROM asset_data WHERE portfolio_id = %s AND date = %s''', (portfolio_id,transaction_datetime,))
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
                    return {"error": "Not enough assets to sell"}, 400
                else:
                    # Calculate and update new amount holding
                    updated_amount_holding = current_amount_holding - transaction_amount
                    updated_cost = cost - transaction_amount * action_price
                    updated_networth = networth - transaction_amount * action_price

            # Insert the transaction into the asset_transactions table
            cursor.execute('''INSERT INTO asset_transactions 
                              (asset_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
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
                           

            # Return a response indicating success
            return {"message": f"{transaction_type} transaction completed successfully, current amount holding:{updated_amount_holding}"}, 200

    
# remove the delete function since we cannot delete a portfolio item
# since its id is using as a foreign key in the asset_data table
# if sell all the shares of the asset, just set the amount_holding to 0
	
    # # delete the asset from the portfolio (i.e. sell all of it)    
    # def delete(self, portfolio_id,transaction_datetime):
    #     with get_db() as db, db.cursor() as cursor:
    #         # get current amount_holding
    #         cursor.execute('''SELECT amount_holding FROM portfolio WHERE id = %s''', (portfolio_id,))
    #         current_amount_holding = cursor.fetchone()[0]
            
    #         # get the latest closing price
    #         cursor.execute('''SELECT close_price
    #                           FROM asset_data
    #                           WHERE portfolio_id = %s
    #                           ORDER BY date DESC
    #                           LIMIT 1''', (portfolio_id,))
    #         transaction_price = cursor.fetchone()[0]
        
    #         # Insert the transaction into the asset_transactions table
    #         cursor.execute('''INSERT INTO asset_transactions 
    #                           (asset_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
    #                           VALUES (%s, %s, %s, %s, %s)''',
    #                        (portfolio_id, "SELL", transaction_datetime, current_amount_holding, transaction_price))
    #         db.commit()
    #         cursor.execute('''DELETE FROM portfolio WHERE id = %s''', (portfolio_id,))
            
    #         db.commit()
    #     return {"message": "Removed asset from portfolio"}, 200


 
api.add_resource(HomeResource, '/')   
api.add_resource(PortfolioResource, '/portfolio')
# api.add_resource(StocksResource, '/stocks')
# api.add_resource(BondsResource, '/bonds')
# api.add_resource(CashResource, '/cash')
api.add_resource(AssetResource, '/portfolio/<int:portfolio_id>')


if __name__ == '__main__':
    app.run()
