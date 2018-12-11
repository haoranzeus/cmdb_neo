from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
print(__name__)
api = Api(app)


class Hello(Resource):
    def get(self):
        return "hello world"
