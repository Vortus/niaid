from flask_restful import Resource, reqparse
from .niaid import *

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
