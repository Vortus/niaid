import datetime
from flask_restful import Resource, reqparse
from .niaid import *

class UserLog(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()
        name = args["name"]
        if (name in users):
            return users[name], 200
        else:
            "club doesn't exist!", 202

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("time")
        parser.add_argument("name")
        parser.add_argument("club")
        args = parser.parse_args()

        name = args["name"]
        club = args["club"]
        loggedTime = int(args["time"])

        bigTime = datetime.datetime.now().strftime(bigFormat)

        if (club not in clubs):
            clubs[club] = {
                "latitude": 0,
                "longitude": 0,
                "log": {}
            }

        addTimeToLog(clubs[club]["log"], bigTime, loggedTime)

        if (name not in users):
            users[name] = {
                "clubs": [
                    club
                ],
                "log": {}
            }

        return "Time logged!", 200
