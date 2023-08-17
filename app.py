from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector

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

api.add_resource(PortfolioResource, '/')



if __name__ == '__main__':
    app.run()
