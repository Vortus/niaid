import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from datetime import datetime, timedelta
from math import floor

app = Flask(__name__)
api = Api(app)

### GENERAL ###
bigFormat = "%Y-%m-%d-%H-%M"
maxTimeUnits = 5
maxTimeRecord = 5 * 60 * 1000#1 * 60 * 60 * 24
maxOnOffTimes = 5 #4 * 24

locations = {
     "Central Tech TDSB - Service Location": {
          "club" : "Toronto Kiwanis Boys and Girls Clubs",
          "address": "725 Bathurst Street\nToronto, ON M5S 2R5",
          "website": "http://www.believeinkids.ca",
          "code": "UTC",
          "log": {
               datetime.now().strftime(bigFormat): {
                    "total" : 10000,
                    "times" : 1
               }
          }
    }
}

users = {
    "John Doe": {
        "locations": [
            "Central Tech TDSB - Service Location"
        ],
        "log": {
            datetime.now().strftime(bigFormat): {
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

class Users(Resource):
     def get(self):
          parser = reqparse.RequestParser()
          parser.add_argument("name")
          args = parser.parse_args()
          name = args["name"]
          if (name in users):
               return users[name], 200
          else:
               "User doesn't exist!", 400

     def post(self):
          parser = reqparse.RequestParser()
          parser.add_argument("time")
          parser.add_argument("name")
          parser.add_argument("location")
          args = parser.parse_args()

          name = args["name"]
          location = args["location"]
          loggedTime = int(args["time"])

          bigTime = datetime.now().strftime(bigFormat)

          if (location not in locations):
               locations[location] = {
                    "latitude": 0,
                    "longitude": 0,
                    "log": {}
               }

          addTimeToLog(locations[location]["log"], bigTime, loggedTime)

          if (name not in users):
               users[name] = {
                    "locations": [
                    location
                    ],
                    "log": {}
               }

          addTimeToLog(users[name]["log"], bigTime, loggedTime)

          return "Time logged!", 200

### PETS ###

def calculatePetHealth(user):
     log = user["log"]
     now = datetime.now()
     onlineTime = 0
     times = 0

     if (now.strftime(bigFormat) in log):
          onlineTime += log[now.strftime(bigFormat)]["total"]
          times += log[now.strftime(bigFormat)]["times"]

     for x in range(1, maxTimeUnits):
          tmpTime = now - timedelta(minutes=x)
          if (tmpTime.strftime(bigFormat) in log):
               onlineTime += log[tmpTime.strftime(bigFormat)]["total"]
               times += log[now.strftime(bigFormat)]["times"]

     mood = round(100 * onlineTime/maxTimeRecord, 0)

     temperment = round(min(100, 100 * times/maxOnOffTimes), 0)

     return {
          "mood": mood,
          "temperment": temperment
     }

class Pets(Resource):
     def get(self):
          parser = reqparse.RequestParser()
          parser.add_argument("name")
          args = parser.parse_args()

          name = args["name"]

          if (name in users):
               return calculatePetHealth(users[name])
          else:
               return "user doesn't exist!", 202

### CLUBS ###
class Locations(Resource):
     def get(self):
          parser = reqparse.RequestParser()
          parser.add_argument("location")
          args = parser.parse_args()
          location = args["location"]
          if (location in locations):
               return locations[location], 200
          else:
               "Location doesn't exist!", 202

     def post(self):
          parser = reqparse.RequestParser()
          parser.add_argument("code")
          args = parser.parse_args()
          code = args["code"]
          for location in locations:
               if (locations[location]["code"] == code):
                    return location, 200
          return "Code invalid!", 202

### FLASK SETUP ###
api.add_resource(Pets, "/pets")
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")

if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0')