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

