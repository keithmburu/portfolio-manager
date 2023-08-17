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
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio''')
        portfolio = cursor.fetchall()
        cursor.close()
        return jsonify(portfolio)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type")
        parser.add_argument("asset_ticker")
        parser.add_argument("asset_name")
        parser.add_argument("amount_holding")
        args = parser.parse_args()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["amount_holding"]))
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
api.add_resource(AssetResource, '/asset/<str:asset_name>')


if __name__ == '__main__':
    app.run()
