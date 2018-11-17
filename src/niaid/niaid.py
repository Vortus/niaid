from flask import Flask
from flask_restful import Api, Resource, reqparse
import datetime

app = Flask(__name__)
api = Api(app)

bigFormat = "%Y-%m-%d-%H"

clubs = {
    "Toronto Central": {
        "latitude": 0,
        "longitude": 0,
        "log": {
            datetime.datetime.now().strftime(bigFormat): {
                "total" : 10000,
                "times" : 1
            }
        }
    }
}

users = {
    "John": {
        "clubs": [
            "Toronto Central"
        ],
        "log": {
            datetime.datetime.now().strftime(bigFormat): {
                "total" : 10000,
                "times" : 1
            }
        }
    }
}

def addTimeToLog(log, stamp, time):
    if (stamp in log):
        log[stamp]["total"] += time
        log[stamp]["times"] += 1
    else:
        log[stamp] = {
            "total": time,
            "times": 1
        }

def calculatePetHealth(user):
    return {
        "mood": 0,
        "temperment": 0
    }

class TimeLog(Resource):
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

api.add_resource(TimeLog, "/log/time")

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

api.add_resource(ClubLog, "/log/club")

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

api.add_resource(UserLog, "/log/user")

class PetStatus(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        name = args["name"]

        if (name in users):
            return calculatePetHealth(users[name])
        else:
            return "user doesn't exist!", 202

api.add_resource(PetStatus, "/pet/status")

app.run(debug=True)