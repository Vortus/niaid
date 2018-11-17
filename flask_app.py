import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
import datetime
from src.niaid.niaid import setup_api

app = Flask(__name__)
api = Api(app)

### GENERAL ###
bigFormat = "%Y-%m-%d-%H"

clubs = {
    "Toronto Central": {
        "address": "test address",
        "code": "UnplugToConnect",
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


### USERS ###

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

### PETS ###

def calculatePetHealth(user):
    return {
        "mood": 0,
        "temperment": 0
    }

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


setup_api(api)

### CLUBS ###
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

     def post(self):
          parser = reqparse.RequestParser()
          parser.add_argument("code")
          args = parser.parse_args()
          code = args["code"]
          for club in clubs:
               if (clubs[club]["code"] == code):
                    return club, 200
          return "Code invalid!", 202

### FLASK SETUP ###
api.add_resource(PetStatus, "/pet/status")
api.add_resource(UserLog, "/log/user")
api.add_resource(ClubLog, "/log/club")

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)