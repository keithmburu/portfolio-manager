from dateutil import parser as dateparser
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)


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
            cursor.execute('''SELECT * FROM portfolio''')
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
                       (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime,currency))

            db.commit()
        resource_url = api.url_for(AssetResource,portfolio_id=cursor.lastrowid, _external=True)
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
            cursor.execute('''SELECT * FROM portfolio WHERE id = %s''', (portfolio_id,))
            portfolio = cursor.fetchone()
        return jsonify({"portfolio":portfolio, "assets":asset})

    def put(self, portfolio_id):
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

        currency = args["currency"] if args["currency"] else None

        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''UPDATE portfolio
                         SET asset_type=%s, asset_ticker=%s, asset_name=%s, amount_holding=%s, buy_datetime=%s, mature_datetime=%s, currency=%s WHERE id=%s''', \
                        (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime,currency, portfolio_id))
            db.commit()
            changed_OK = {"message": "Asset updated successfully"}, 200
            not_found = {"error": "Asset not found"}, 404
            json = changed_OK if cursor.rowcount else not_found
        return json
	    
    def delete(self, portfolio_id):
        with get_db() as db, db.cursor() as cursor:
            cursor.execute('''DELETE FROM portfolio WHERE id = %s''', (portfolio_id,))
            cursor.execute('''DELETE FROM asset_data WHERE portfolio_id = %s''', (portfolio_id,))
            db.commit()
        return {"message": "Removed asset from portfolio"}, 200


    
api.add_resource(PortfolioResource, '/')
api.add_resource(StocksResource, '/stocks')
api.add_resource(BondsResource, '/bonds')
api.add_resource(CashResource, '/cash')
api.add_resource(AssetResource, '/<int:portfolio_id>')


if __name__ == '__main__':
    app.run()
