from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector
from datetime import datetime
import dateutil.parser

app = Flask(__name__)
api = Api(app)


db = mysql.connector.connect(
        host="localhost",
        user="training",
        password="1234567A",
    )

class PortfolioResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''USE portfolio''')
        cursor.execute('''SELECT * FROM portfolio''')
        portfolio = cursor.fetchall()
        cursor.close()
        return jsonify(portfolio)
    
    # user add new item to the portfolio
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type", required=True)
        parser.add_argument("asset_ticker", required=True)
        parser.add_argument("asset_name", required=True)
        parser.add_argument("volume", required=True, type=int)
        parser.add_argument("buy_datetime", required=True)
        parser.add_argument("mature_datetime")
        parser.add_argument("currency")
        args = parser.parse_args()

        asset_type = args["asset_type"].upper()
        asset_ticker = args["asset_ticker"].upper()
        asset_name = args["asset_name"].upper()
        volume = args["volume"]
        
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
                          (asset_type, asset_ticker, asset_name, volume, start_datetime, mature_datetime, currency)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (asset_type, asset_ticker, asset_name, volume, buy_datetime, mature_datetime,currency))

        db.commit()
        cursor.close()
        return {"message": "Added new asset to portfolio"}, 201



api.add_resource(PortfolioResource, '/')


if __name__ == '__main__':
    app.run()
