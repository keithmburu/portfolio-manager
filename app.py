from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)


db = mysql.connector.connect(
        host="localhost",
        user="nora_training",
        password="1234567A",
        database="conygre"
    )

class PortfolioResource(Resource):
    def get(self):
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM portfolio''')
        portfolio = cursor.fetchall()
        cursor.close()
        return jsonify(portfolio)


api.add_resource('/', PortfolioResource)


if __name__ == '__main__':
    app.run()
