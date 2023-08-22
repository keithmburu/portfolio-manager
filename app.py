from dateutil import parser as dateparser
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector
from flask_cors import CORS 

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


class PortfolioResource(Resource):
    def get(self):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM portfolio WHERE amount_holding > 0''')
            portfolio = cursor.fetchall()
            cursor.execute('''SELECT * FROM historical_networth''')
            networth = cursor.fetchall()
        return jsonify({"portfolio":portfolio, "networth":networth})

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

        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''INSERT INTO portfolio 
                          (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime, currency))

            # Retrieve the last inserted row's ID
            portfolio_id = cursor.lastrowid
            
            cursor.execute('''SELECT price FROM asset_data WHERE portfolio_id = %s AND date = %s''', (portfolio_id,buy_datetime,))
            action_price = cursor.fetchone()[0]
            # Insert the transaction into the asset_transactions table
            cursor.execute('''INSERT INTO asset_transactions 
                              (asset_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (portfolio_id, 'BUY', buy_datetime, amount_holding, action_price))  # Example transaction_price

            db.commit()

        resource_url = api.url_for(AssetResource, portfolio_id=portfolio_id, _external=True)
        insert_ok = ({"message": "Added new asset to portfolio"}, 201, {"Location": f"{resource_url}"})
        insert_failed = ({"message": "Failed to add new asset to portfolio"}, 400)
        return insert_ok if cursor.rowcount else insert_failed



class StocksResource(Resource):
    def get(self):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM portfolio WHERE asset_type = stock''')
            stocks = cursor.fetchall()
        return jsonify(stocks)


class BondsResource(Resource):
    def get(self):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM portfolio WHERE asset_type = bond''')
            bonds = cursor.fetchall()
        return jsonify(bonds)


class CashResource(Resource):
    def get(self):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM portfolio WHERE asset_type = cash''')
            cash = cursor.fetchall()
        return jsonify(cash)


class AssetResource(Resource):
    def get(self, portfolio_id):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''SELECT * FROM asset_data WHERE portfolio_id = %s''', (portfolio_id,))
            asset = cursor.fetchall()
            cursor.execute('''SELECT * FROM asset_transactions WHERE asset_id = %s''', (portfolio_id,))
            transactions = cursor.fetchall()
            cursor.execute('''SELECT * FROM portfolio WHERE id = %s''', (portfolio_id,))
            portfolio = cursor.fetchone()
        return jsonify({"portfolio":portfolio, "assets":asset,"transactions": transactions})

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
            cursor.execute('''SELECT amount_holding FROM portfolio WHERE id = %s''', (portfolio_id,))
            current_amount_holding = cursor.fetchone()[0]
            
            # get the current price for the asset
            cursor.execute('''SELECT price FROM asset_data WHERE portfolio_id = %s AND date = %s''', (portfolio_id,transaction_datetime,))
            action_price = cursor.fetchone()[0]
            
            # get the current networth for the portfolio
            cursor.execute('''SELECT networth FROM historical_networth WHERE date = %s''', (transaction_datetime,))
            networth = cursor.fetchone()[0]
            
            if transaction_type == "BUY":
                # Calculate and update new amount holding
                updated_amount_holding = current_amount_holding + transaction_amount
            elif transaction_type == "SELL":
                if transaction_amount > current_amount_holding:
                    return {"error": "Not enough assets to sell"}, 400
                else:
                    # Calculate and update new amount holding
                    updated_amount_holding = current_amount_holding - transaction_amount

            # Insert the transaction into the asset_transactions table
            cursor.execute('''INSERT INTO asset_transactions 
                              (asset_id, transaction_type, transaction_datetime, transaction_amount, transaction_price)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (portfolio_id, transaction_type, transaction_datetime, transaction_amount, action_price))
            db.commit()

            # Update the portfolio's amount_holding after transaction
            cursor.execute('''UPDATE portfolio SET amount_holding=%s WHERE id=%s''',
                           (updated_amount_holding, portfolio_id))
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


    
api.add_resource(PortfolioResource, '/')
api.add_resource(StocksResource, '/stocks')
api.add_resource(BondsResource, '/bonds')
api.add_resource(CashResource, '/cash')
api.add_resource(AssetResource, '/<int:portfolio_id>')


if __name__ == '__main__':
    app.run()
