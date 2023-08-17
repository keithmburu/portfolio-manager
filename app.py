import dateutil
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)


db = mysql.connector.connect(
        host="localhost",
        user="training",
        password="1234567A",
        database="TAPHK"
    )


class PortfolioResource(Resource):
    # only for stock for now
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio''')
        portfolio = cursor.fetchall()
        cursor.close()
        return jsonify(portfolio)

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

        asset_type = args["asset_type"].upper()
        asset_ticker = args["asset_ticker"].upper()
        asset_name = args["asset_name"].upper()
        amount_holding = args["amount_holding"]
        
        try:
            # Parse start_datetime using dateutil.parser
            buy_datetime = dateutil.parser.parse(args["buy_datetime"])
        except Exception as e:
            return {"error": "Invalid buy_datetime format"}, 400
        
        if args["mature_datetime"]:
            try:
                # Parse mature_datetime using dateutil.parser
                mature_datetime = dateutil.parser.parse(args["mature_datetime"])
            except Exception as e:
                return {"error": "Invalid mature_datetime format"}, 400
        else:
            mature_datetime = None

        currency = args["currency"].upper() if args["currency"] else None
        
        cursor = db.cursor()
        cursor.execute('''INSERT INTO portfolio 
                          (asset_type, asset_ticker, asset_name, amount_holding, start_datetime, mature_datetime, currency)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (asset_type, asset_ticker, asset_name, amount_holding, buy_datetime, mature_datetime,currency))

        db.commit()
        cursor.close()
        return {"message": "Added new asset to portfolio"}, 201


class StocksResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio WHERE asset_type = stock''')
        stocks = cursor.fetchall()
        cursor.close()
        return jsonify(stocks)


class BondsResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio WHERE asset_type = bond''')
        bonds = cursor.fetchall()
        cursor.close()
        return jsonify(bonds)


class CashResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio WHERE asset_type = cash''')
        cash = cursor.fetchall()
        cursor.close()
        return jsonify(cash)


class AssetResource(Resource):
    def get(self, asset_name):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM asset_data WHERE asset_name = %s''', (asset_name,))
        timeseries = cursor.fetchall()
        cursor.close()
        return jsonify(timeseries)

    def delete(self, asset_name):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_name")
        args = parser.parse_args()
        cursor = db.cursor()
        cursor.execute('''DELETE FROM portfolio WHERE asset_name = %s''', (args["asset_name"],))
        db.commit()
        cursor.close()
        return {"message": "Removed asset from portfolio"}, 200


    
api.add_resource(PortfolioResource, '/')
api.add_resource(StocksResource, '/stocks')
api.add_resource(BondsResource, '/bonds')
api.add_resource(CashResource, '/cash')
api.add_resource(AssetResource, '/asset/<int:asset_name>')


if __name__ == '__main__':
    app.run()
