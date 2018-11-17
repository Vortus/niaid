import datetime
from .pets import PetStatus
from .users import UserLog
from .clubs import ClubLog

def setup_api(api):
    api.add_resource(PetStatus, "/pet/status")
    api.add_resource(UserLog, "/log/user")
    api.add_resource(ClubLog, "/log/club")

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
