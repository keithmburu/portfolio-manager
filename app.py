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
        cursor.execute('''USE portfolio''')
        cursor.execute('''SELECT * FROM portfolio''')
        portfolio = cursor.fetchall()
        cursor.close()
        return jsonify(portfolio)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asset_type")
        parser.add_argument("stock_ticker")
        parser.add_argument("company_name")
        parser.add_argument("volume")
        args = parser.parse_args()
        cursor = db.cursor()
        cursor.execute('''USE portfolio''')
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["volume"]))
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
        cursor.execute('''USE portfolio''')
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
        cursor.execute('''USE portfolio''')
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
        cursor.execute('''USE portfolio''')
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["volume"]))
        db.commit()
        cursor.close()
        return {"message": "Added new cash to portfolio"}, 201


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
        cursor.execute('''USE portfolio''')
        cursor.execute('''INSERT INTO portfolio VALUES (%s, %s, %s, %s)''', \
                        (args["asset_type"], args["stock_ticker"], args["company_name"], args["volume"]))
        db.commit()
        cursor.close()
        return {"message": "Added new cash to portfolio"}, 201

api.add_resource(PortfolioResource, '/')
api.add_resource(StocksResource, '/stocks')
api.add_resource(BondsResource, '/bonds')
api.add_resource(CashResource, '/cash')


if __name__ == '__main__':
    app.run()
