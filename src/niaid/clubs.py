from flask_restful import Resource, reqparse
from .niaid import *

class ClubLog(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("club")
        args = parser.parse_args()
        club = args["club"]
        if (club in clubs):
            return clubs[club], 200
        else:
            "club doesn't exist!", 202
