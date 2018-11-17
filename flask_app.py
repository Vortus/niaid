import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
import datetime

app = Flask(__name__)
api = Api(app)

### GENERAL ###
bigFormat = "%Y-%m-%d-%H"

locations = {
     "Central Tech TDSB - Service Location": {
          "club" : "Toronto Kiwanis Boys and Girls Clubs",
          "address": "725 Bathurst Street\nToronto, ON M5S 2R5",
          "website": "http://www.believeinkids.ca",
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
    "John Doe": {
        "locations": [
            "Central Tech TDSB - Service Location"
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

          bigTime = datetime.datetime.now().strftime(bigFormat)

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
     return {
          "mood": 0,
          "temperment": 0
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
          code = args["location"]
          for location in locations:
               if (locations[location]["code"] == code):
                    return locations[location], 200
          return "Code invalid!", 202

### FLASK SETUP ###
api.add_resource(Pets, "/pets")
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")

if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0')