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
        database="TAPHK"
    )

class PortfolioResource(Resource):
    # only for stock for now
    def update_net_worth(self):
        query = """
        UPDATE portfolio P
        JOIN (
            SELECT P.asset_name,
                    SUM
        )
        """
        
    def get(self):
        cursor = db.cursor()
        cursor.execute('''
                       UPDATE portfolio P
                       INNER JOIN 
                       ''')
    
    # user add new item to the portfolio
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
        cursor.execute('''USE portfolio''')
        cursor.execute('''SELECT * FROM portfolio WHERE asset_type = stock''')
        stocks = cursor.fetchall()
        cursor.close()
        return jsonify(stocks)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type")
        parser.add_argument("stock_ticker")
        parser.add_argument("company_name")
        parser.add_argument("volume")
        args = parser.parse_args()
        cursor = db.cursor()
        cursor.execute('''USE stocks''')
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["volume"]))
        db.commit()
        cursor.close()
        return {"message": "Added new stock to portfolio"}, 201


class BondsResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio WHERE asset_type = bond''')
        bonds = cursor.fetchall()
        cursor.close()
        return jsonify(bonds)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type")
        parser.add_argument("stock_ticker")
        parser.add_argument("company_name")
        parser.add_argument("volume")
        args = parser.parse_args()
        cursor = db.cursor()
        cursor.execute('''USE bonds''')
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["volume"]))
        db.commit()
        cursor.close()
        return {"message": "Added new bond to portfolio"}, 201


class CashResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''USE portfolio''')
        cursor.execute('''SELECT * FROM portfolio WHERE asset_type = cash''')
        cash = cursor.fetchall()
        cursor.close()
        return jsonify(cash)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type")
        parser.add_argument("stock_ticker")
        parser.add_argument("company_name")
        parser.add_argument("volume")
        args = parser.parse_args()
        cursor = db.cursor()
        cursor.execute('''USE cash''')
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["volume"]))
        db.commit()
        cursor.close()
        return {"message": "Added new cash to portfolio"}, 201


api.add_resource(PortfolioResource, '/')
api.add_resource(StocksResource, '/stocks')
api.add_resource(BondsResource, '/bonds')
api.add_resource(CashResource, '/cash')

api.add_resource(PortfolioResource, '/')


if __name__ == '__main__':
    app.run()
