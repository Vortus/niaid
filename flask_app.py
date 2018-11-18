import os
from flask import Flask, Response
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from datetime import datetime, timedelta
from math import floor
import json
import pytz

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

### GENERAL ###
bigFormat = "%Y-%m-%d-%H-%M"
maxTimeUnits = 5
maxTimeRecord = 6 * 60 * 1000#1 * 60 * 60 * 24
maxOnOffTimes = 10 #4 * 24

locations = {
     "Central Tech TDSB - Service Location": {
          "club" : "Toronto Kiwanis Boys and Girls Clubs",
          "address": "725 Bathurst Street\nToronto, ON M5S 2R5",
          "website": "http://www.believeinkids.ca",
          "code": "UTC",
          "log": {
          }
    }
}

fakeResponse = [
  {
    "Location": "John Tod Centre Boys and Girls Club - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 299
  },
  {
    "Location": "Ontario Early Years Centre- Hamilton East Main Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 299
  },
  {
    "Location": "College Park BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 299
  },
  {
    "Location": "Norris Arm Boys and Girls Club - Main Club",
    "Club": "Norris Arm Boys and Girls Club",
    "Total time offline in mins": 298
  },
  {
    "Location": "Bishop Roborecki BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 297
  },
  {
    "Location": "Dovercourt Clubhouse - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 297
  },
  {
    "Location": "C.E. Broughton Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 296
  },
  {
    "Location": "Central Saanich Club - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 296
  },
  {
    "Location": "Parents Together - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 296
  },
  {
    "Location": "Uxbridge Library - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 295
  },
  {
    "Location": "Don McGahan Clubhouse - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 295
  },
  {
    "Location": "Oliver Boys and Girls Clubs - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 295
  },
  {
    "Location": "Viscount Alexander - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 294
  },
  {
    "Location": "Youth Mentorship Program - Why Not Youth Centre - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 294
  },
  {
    "Location": "Boys and Girls Club of Yarmouth - Main Club",
    "Club": "Boys and Girls Club of Yarmouth",
    "Total time offline in mins": 294
  },
  {
    "Location": "Station 4 Daycare (Chase River Location) - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 293
  },
  {
    "Location": "Youth Mentorship Program - Camp Unity - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 292
  },
  {
    "Location": "Boys and Girls Club of Cochrane and Area - Main Club",
    "Club": "Boys and Girls Club of Cochrane and Area",
    "Total time offline in mins": 292
  },
  {
    "Location": "Let's Get Moving- Green Acres School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 292
  },
  {
    "Location": "Salisbury Boys and Girls Club Inc. - Main Club",
    "Club": "Salisbury Boys and Girls Club Inc.",
    "Total time offline in mins": 291
  },
  {
    "Location": "Benalto - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 290
  },
  {
    "Location": "Ron Kolbus Clubhouse - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 289
  },
  {
    "Location": "James Hornell Boys and Girls Club - Main Club",
    "Club": "James Hornell Boys and Girls Club",
    "Total time offline in mins": 289
  },
  {
    "Location": "Rexdale Community Hub  - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 288
  },
  {
    "Location": "Dovercourt Boys and Girls Club - Main Club",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 288
  },
  {
    "Location": "Woodville Club at Woodville Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 287
  },
  {
    "Location": "Silverthorn Community School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 287
  },
  {
    "Location": "General Vanier - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 286
  },
  {
    "Location": "Joyceville Public School - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 286
  },
  {
    "Location": "Blacks Harbour Elementary School - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 285
  },
  {
    "Location": "Bobby Orr Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 285
  },
  {
    "Location": "Castlebrook - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 284
  },
  {
    "Location": "L'Azimut de Courville - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 284
  },
  {
    "Location": "Africa Centre - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 283
  },
  {
    "Location": "McHugh Public School - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 280
  },
  {
    "Location": "Boys and Girls Club of Sarnia/Lambton - Main Club",
    "Club": "Boys and Girls Club of Sarnia/Lambton",
    "Total time offline in mins": 280
  },
  {
    "Location": "Crystal Beach Satellite At St. George Catholic Elementary School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 279
  },
  {
    "Location": "Beurling Academy - Service Location",
    "Club": "Boys and Girls Clubs of Dawson",
    "Total time offline in mins": 279
  },
  {
    "Location": "Boys and Girls Clubs of Saskatoon - Main Club",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 279
  },
  {
    "Location": "Boys and Girls Clubs of Thunder Bay - Main Club",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 279
  },
  {
    "Location": "Maison des jeunes de Sillery - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 279
  },
  {
    "Location": "St. Thomas More Afterschool Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 278
  },
  {
    "Location": "Roland Michener BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 278
  },
  {
    "Location": "Lavington Elementary School Afterschool PRogram - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 278
  },
  {
    "Location": "Stettler & District Boys and Girls Club - Main Club",
    "Club": "Stettler & District Boys and Girls Club",
    "Total time offline in mins": 278
  },
  {
    "Location": "Riverview Middle School - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 277
  },
  {
    "Location": "Odyssey II - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 277
  },
  {
    "Location": "Winona Senior Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 277
  },
  {
    "Location": "Black Diamond - Service Location",
    "Club": "Boys and Girls Clubs of the Foothills",
    "Total time offline in mins": 276
  },
  {
    "Location": "Rexdale Community Hub - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 275
  },
  {
    "Location": "E.A. Fairman Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 275
  },
  {
    "Location": "Bramalea S. S. - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 275
  },
  {
    "Location": "Boys and Girls Club of Red Deer and District - Main Club",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 275
  },
  {
    "Location": "L'Intégrale Sud - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 275
  },
  {
    "Location": "Kiddy Korner Daycare/Tod/Preschool/Before & ASP - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 273
  },
  {
    "Location": "Second Harvest Kitchen - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 273
  },
  {
    "Location": "Boys and Girls Club of Peel - Main Club",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 273
  },
  {
    "Location": "Braeburn Boys and Girls Club - Main Club",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 273
  },
  {
    "Location": "Braeburn Junior School - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 273
  },
  {
    "Location": "Highfield Junior School - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 272
  },
  {
    "Location": "Marie Sharpe Elementary School - Service Location",
    "Club": "Boys and Girls Club of Williams Lake and District",
    "Total time offline in mins": 272
  },
  {
    "Location": "Elmlea Junior School - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 272
  },
  {
    "Location": "Mons. John Pereyman Catholic SS - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 271
  },
  {
    "Location": "Family Centre Westmount - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 270
  },
  {
    "Location": "Maison des jeunes de Notre-Dame des Monts - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 270
  },
  {
    "Location": "MDJ St-Siméon - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 270
  },
  {
    "Location": "Comox Valley Parent Services - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 269
  },
  {
    "Location": "Holy Rosary Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 269
  },
  {
    "Location": "Emmett Avenue Summer Program - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 269
  },
  {
    "Location": "Bishop Filevich BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 268
  },
  {
    "Location": "Henry St Clubhouse - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 267
  },
  {
    "Location": "St. James Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 267
  },
  {
    "Location": "Lets Get Moving - St. David's School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 267
  },
  {
    "Location": "Integrated Family Development Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 267
  },
  {
    "Location": "Ontario Early Years Centre -- Elizabeth Bagshaw Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 266
  },
  {
    "Location": "North Glenmore Elementary School Preschool and Afterschool - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 266
  },
  {
    "Location": "Northview Unit - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 265
  },
  {
    "Location": "Riverview East School - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 265
  },
  {
    "Location": "Youth Mentorship Program - Woodview Mental Health - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 264
  },
  {
    "Location": "St. Margaret's Afterschool Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 263
  },
  {
    "Location": "Gloria hayden community centre - Service Location",
    "Club": "Boys and Girls Club of Yorkton Inc.",
    "Total time offline in mins": 262
  },
  {
    "Location": "Polson Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 262
  },
  {
    "Location": "Bowden Kids Club - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 261
  },
  {
    "Location": "Weekday Warriors - Elijah Smith Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Yukon",
    "Total time offline in mins": 261
  },
  {
    "Location": "Kinsmen Pool - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 260
  },
  {
    "Location": "Elnora - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 260
  },
  {
    "Location": "Boys and Girls Club of St. Paul & District - Main Club",
    "Club": "Boys and Girls Club of St. Paul & District",
    "Total time offline in mins": 260
  },
  {
    "Location": "Beau Valley Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 259
  },
  {
    "Location": "Eastview (Toronto) Boys and Girls Club - Main Club",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 259
  },
  {
    "Location": "Summerland Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 259
  },
  {
    "Location": "Rawlinson Community School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 259
  },
  {
    "Location": "Community of Christ Church - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 258
  },
  {
    "Location": "Let's Get Moving- Viscount Montgomery School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 258
  },
  {
    "Location": "Parents Together - Safehouse - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 258
  },
  {
    "Location": "Father Robinson BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 257
  },
  {
    "Location": "Camp Potlatch - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 257
  },
  {
    "Location": "Kids in Motion Licensed Child Care At Dr George Hall Public School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 256
  },
  {
    "Location": "Wintemute Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 256
  },
  {
    "Location": "Fairview Kids Club - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 255
  },
  {
    "Location": "Webber Road Community Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 255
  },
  {
    "Location": "Warren Park Junior Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 255
  },
  {
    "Location": "Camrose and District Boys and Girls Club - Main Club",
    "Club": "Camrose and District Boys and Girls Club",
    "Total time offline in mins": 254
  },
  {
    "Location": "Prime Time - Service Location",
    "Club": "Cranbrook Boys and Girls Club",
    "Total time offline in mins": 254
  },
  {
    "Location": "Lake Country Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 254
  },
  {
    "Location": "St. Peter's Elementary School - Service Location",
    "Club": "Upper Island Cove Boys and Girls Club",
    "Total time offline in mins": 254
  },
  {
    "Location": "Corpus Christi School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 253
  },
  {
    "Location": "St. Stephen Middle School - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 252
  },
  {
    "Location": "North West Scarborough Youth Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 252
  },
  {
    "Location": "Boys and Girls Clubs of Calgary - Main Club",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 252
  },
  {
    "Location": "Boys and Girls Clubs of Hamilton - Main Club",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 252
  },
  {
    "Location": "Boys and Girls Club of West Scarborough - Main Club",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 251
  },
  {
    "Location": "Saskatoon Christian BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 251
  },
  {
    "Location": "Maison des jeunes du Lac-Beauport - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 251
  },
  {
    "Location": "North Kipling Junior Middle School - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 250
  },
  {
    "Location": "G.L. Roberts CVI  - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 250
  },
  {
    "Location": "Arthur Hatton School - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 250
  },
  {
    "Location": "Woodbine Shopping Centre  - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 250
  },
  {
    "Location": "Rideau High School - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 249
  },
  {
    "Location": "Woodbridge Public School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 249
  },
  {
    "Location": "Chemainus Club - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 249
  },
  {
    "Location": "North Kipling Community Centre  - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 249
  },
  {
    "Location": "Avenue 15 - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 248
  },
  {
    "Location": "St. Frances Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 248
  },
  {
    "Location": "Stepping Stones Daycare - Service Location",
    "Club": "Cranbrook Boys and Girls Club",
    "Total time offline in mins": 248
  },
  {
    "Location": "Main Club House - Service Location",
    "Club": "Fort McMurray Boys and Girls Club",
    "Total time offline in mins": 248
  },
  {
    "Location": "Maison des jeunes l'Ambassade du Lac St-Charles - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 248
  },
  {
    "Location": "Boys and Girls Club of Brantford - Main Club",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 245
  },
  {
    "Location": "Maison des jeunes de St-Augustin-de-Desmaures - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 245
  },
  {
    "Location": "Fairbank Middle School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 245
  },
  {
    "Location": "The Refuge - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 244
  },
  {
    "Location": "Brocklehurst Neighbourhood Club - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 244
  },
  {
    "Location": "Oakridge Public School - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 244
  },
  {
    "Location": "Sir William Mulock Secondary School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 244
  },
  {
    "Location": "Clarence Sansom Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 243
  },
  {
    "Location": "St.James Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 243
  },
  {
    "Location": "Earl Beatty Public School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 243
  },
  {
    "Location": "Morningside Library - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 242
  },
  {
    "Location": "Mahmawi-atoskiwin (Aboriginal Partnership) - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 242
  },
  {
    "Location": "Surrey Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 242
  },
  {
    "Location": "Joannes House-Youth Housing - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 241
  },
  {
    "Location": "Pond Mills - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 241
  },
  {
    "Location": "Oakridge Public School - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 241
  },
  {
    "Location": "Boys and Girls Club Services of Greater Victoria - Main Club",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 241
  },
  {
    "Location": "Orton Park Learning Centre - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 239
  },
  {
    "Location": "Youth Impact Youth Centre - Service Location",
    "Club": "Cranbrook Boys and Girls Club",
    "Total time offline in mins": 239
  },
  {
    "Location": "Boys and Girls Clubs of Central Vancouver Island - Main Club",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 238
  },
  {
    "Location": "St. Rita Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 237
  },
  {
    "Location": "Youth and Volunteer Centre - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 236
  },
  {
    "Location": "Harbourside Esquimalt Club - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 236
  },
  {
    "Location": "Clarke High School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 235
  },
  {
    "Location": "Nanton - Service Location",
    "Club": "Boys and Girls Clubs of the Foothills",
    "Total time offline in mins": 235
  },
  {
    "Location": "Youthwise - Service Location",
    "Club": "Cranbrook Boys and Girls Club",
    "Total time offline in mins": 235
  },
  {
    "Location": "Badke Suites - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 235
  },
  {
    "Location": "Joseph Brant After School Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 234
  },
  {
    "Location": "Steinhauer Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 234
  },
  {
    "Location": "The Lodge (Program/Office Space) - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 234
  },
  {
    "Location": "Let's Get Moving- W.H. Ballard Public School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 234
  },
  {
    "Location": "Cameron Park Early Learning Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 234
  },
  {
    "Location": "Maison des jeunes de Ste-Foy - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 234
  },
  {
    "Location": "Boys & Girls Club of Wolf Creek - Ponoka - Main Club",
    "Club": "Boys & Girls Club of Wolf Creek - Ponoka",
    "Total time offline in mins": 233
  },
  {
    "Location": "Algonquin School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 232
  },
  {
    "Location": "Linklater Public School - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 231
  },
  {
    "Location": "Stevensville Satellite St. Joseph Catholic School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 231
  },
  {
    "Location": "Ready - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 231
  },
  {
    "Location": "Albion Public Library  - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 231
  },
  {
    "Location": "Brampton Towers - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 230
  },
  {
    "Location": "RRTG Location - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 230
  },
  {
    "Location": "Maison des jeunes de St-Ferréol-Les-Neiges - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 230
  },
  {
    "Location": "Lower Sahali Neighbourhood Club - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 229
  },
  {
    "Location": "Penbrooke Meadows Club - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 229
  },
  {
    "Location": "St. Peter's Elementary School - Service Location",
    "Club": "Upper Island Cove Boys and Girls Club",
    "Total time offline in mins": 229
  },
  {
    "Location": "Coverdale Center - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 228
  },
  {
    "Location": "South Side Teen Centre - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 228
  },
  {
    "Location": "NGEN Youth Centre - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 228
  },
  {
    "Location": "St. Jude School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 228
  },
  {
    "Location": "Weekday Warrios - Ecole Whitehorse Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Yukon",
    "Total time offline in mins": 228
  },
  {
    "Location": "Harmony Heights Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 226
  },
  {
    "Location": "Central Public School - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 225
  },
  {
    "Location": "Boys and Girls Club of Wasaga Beach - Service Location",
    "Club": "Boys and Girls Clubs of North Simcoe",
    "Total time offline in mins": 225
  },
  {
    "Location": "Let's Get Moving- Parkdale School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 224
  },
  {
    "Location": "Henry Street High School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 223
  },
  {
    "Location": "Freight House Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 223
  },
  {
    "Location": "Boys and Girls Club of Niagara - Main Club",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 222
  },
  {
    "Location": "Heloise Lorimer  - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 221
  },
  {
    "Location": "Boys and Girls Club of Leduc - Main Club",
    "Club": "Boys and Girls Club of Leduc",
    "Total time offline in mins": 221
  },
  {
    "Location": "Ryerson Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 221
  },
  {
    "Location": "Learning Tree Daycare - Service Location",
    "Club": "Boys and Girls Clubs of Yukon",
    "Total time offline in mins": 221
  },
  {
    "Location": "Holy Name School - Service Location",
    "Club": "Boys and Girls Club of Pembroke",
    "Total time offline in mins": 220
  },
  {
    "Location": "Claude Garton School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 220
  },
  {
    "Location": "Springbrook - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 219
  },
  {
    "Location": "Purnell Boys & Girls Club - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 219
  },
  {
    "Location": "Warman BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 219
  },
  {
    "Location": "Grandview Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 219
  },
  {
    "Location": "Topcliff Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 219
  },
  {
    "Location": "North Dartmouth - Service Location",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 218
  },
  {
    "Location": "Boys and Girls Club of Airdrie - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 218
  },
  {
    "Location": "Durham Mental Health Shelter - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 218
  },
  {
    "Location": "Rundle Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 218
  },
  {
    "Location": "Let's Get Moving- Blessed Kateri School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 218
  },
  {
    "Location": "Langley Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 218
  },
  {
    "Location": "Winskill Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 218
  },
  {
    "Location": "Maison des jeunes de Sainte-Catherine-de-la-Jacques-Cartier - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 218
  },
  {
    "Location": "North Delta Family Resource Centre - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 217
  },
  {
    "Location": "Baycrest Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 217
  },
  {
    "Location": "Ajax Community Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 216
  },
  {
    "Location": "Highland Creek Library - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 216
  },
  {
    "Location": "Birchmount Bluffs Neighbourhood Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 216
  },
  {
    "Location": "Richardson Road - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 215
  },
  {
    "Location": "Summer in the City Day Camp East - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 213
  },
  {
    "Location": "Glenbow Club - Service Location",
    "Club": "Boys and Girls Club of Cochrane and Area",
    "Total time offline in mins": 212
  },
  {
    "Location": "Rochester Heights - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 212
  },
  {
    "Location": "Boys and Girls Club of Sarnia Lambton - Service Location",
    "Club": "Boys and Girls Club of Sarnia/Lambton",
    "Total time offline in mins": 212
  },
  {
    "Location": "Kirkfield Club At Lady MacKenzie Public School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 212
  },
  {
    "Location": "Highfield Community Enrichment Project  - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 212
  },
  {
    "Location": "St. Luigi Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 212
  },
  {
    "Location": "Boys and Girls Club of Fredericton - Main Club",
    "Club": "Boys and Girls Club of Fredericton",
    "Total time offline in mins": 210
  },
  {
    "Location": "Erin Court - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 210
  },
  {
    "Location": "St. Anthony's School - Service Location",
    "Club": "Boys and Girls Club of Pembroke",
    "Total time offline in mins": 210
  },
  {
    "Location": "College Park Preschool - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 210
  },
  {
    "Location": "Boys and Girls Clubs of St. John's - Main Club",
    "Club": "Boys and Girls Clubs of St. John's",
    "Total time offline in mins": 209
  },
  {
    "Location": "Carmi Elementary School - After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 209
  },
  {
    "Location": "Cedar Creek Afterschool Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 209
  },
  {
    "Location": "Let's Get Moving- Strathcona - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 208
  },
  {
    "Location": "Maison des jeunes de l'Ancienne-Lorette - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 208
  },
  {
    "Location": "West Nissouri PS - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 207
  },
  {
    "Location": "St. George Elementary - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 206
  },
  {
    "Location": "Boys and Girls Club of York Region - Main Club",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 206
  },
  {
    "Location": "Pineridge Club - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 205
  },
  {
    "Location": "Boys and Girls Clubs of South Coast BC - Main Club",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 205
  },
  {
    "Location": "Grand Manan Community School - Service Location",
    "Club": "The Boys and Girls Club of Grand Manan Island Inc.",
    "Total time offline in mins": 205
  },
  {
    "Location": "Youth Centre - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 204
  },
  {
    "Location": "Bobcaygeon Club at BobcaygeonPublic School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 204
  },
  {
    "Location": "Rocky Youth Development Society - Service Location",
    "Club": "Clearwater Boys and Girls Club",
    "Total time offline in mins": 204
  },
  {
    "Location": "Oliver Youth Centre at the Hangar - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 204
  },
  {
    "Location": "Leslie Junior Public School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 203
  },
  {
    "Location": "Trimbee TCHC  - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 203
  },
  {
    "Location": "East Dartmouth - Service Location",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 202
  },
  {
    "Location": "St. Dominic Afterschool Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 202
  },
  {
    "Location": "Archbishop Romero Catholic H.S. - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 202
  },
  {
    "Location": "Alexander Graham Bell Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 201
  },
  {
    "Location": "St. Anthony and Area Boys and Girls Club - Main Club",
    "Club": "St. Anthony and Area Boys and Girls Club",
    "Total time offline in mins": 201
  },
  {
    "Location": "Dallas Afterschool Club - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 199
  },
  {
    "Location": "Duggan Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 199
  },
  {
    "Location": "Pineridge Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 199
  },
  {
    "Location": "Adult Day Program - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 199
  },
  {
    "Location": "St. Stephen Elementary School - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 198
  },
  {
    "Location": "Mason Road After School - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 198
  },
  {
    "Location": "Kids First Child Care At Prince of Wales Public School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 198
  },
  {
    "Location": "Yorkton Public Library - Service Location",
    "Club": "Boys and Girls Club of Yorkton Inc.",
    "Total time offline in mins": 198
  },
  {
    "Location": "Bishop Klein BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 198
  },
  {
    "Location": "Norris Arm Service Location - Service Location",
    "Club": "Norris Arm Boys and Girls Club",
    "Total time offline in mins": 198
  },
  {
    "Location": "Alton Towers Co-Op - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 196
  },
  {
    "Location": "Carpathia Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 196
  },
  {
    "Location": "St. Mary's of the Angels - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 196
  },
  {
    "Location": "EYC Centre Parade Street - Service Location",
    "Club": "Boys and Girls Club of Yarmouth",
    "Total time offline in mins": 195
  },
  {
    "Location": "High River - After School Location - Service Location",
    "Club": "Boys and Girls Clubs of the Foothills",
    "Total time offline in mins": 195
  },
  {
    "Location": "Vale Unit - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 195
  },
  {
    "Location": "Gilbert Park Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 195
  },
  {
    "Location": "Maison des jeunes de Québec (OBQ) - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 194
  },
  {
    "Location": "Boys and Girls Club of Williams Lake and District - Main Club",
    "Club": "Boys and Girls Club of Williams Lake and District",
    "Total time offline in mins": 193
  },
  {
    "Location": "Orillia Public Library - Service Location",
    "Club": "Boys and Girls Clubs of North Simcoe",
    "Total time offline in mins": 193
  },
  {
    "Location": "Langham Elementary BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 193
  },
  {
    "Location": "Holy Cross Catholic Elementary School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 193
  },
  {
    "Location": "Albion Neighbourhood Services Boys and Girls Club - Main Club",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 192
  },
  {
    "Location": "South Oshawa Community Support Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 192
  },
  {
    "Location": "Junction Triangle Clubhouse - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 192
  },
  {
    "Location": "Régional des maisons de jeunes de Québec - Main Club",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 192
  },
  {
    "Location": "Boys & Girls Club of Cornwall - Main Club",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 191
  },
  {
    "Location": "Sackville - Service Location",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 191
  },
  {
    "Location": "John M. James Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 191
  },
  {
    "Location": "St. Mark Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 191
  },
  {
    "Location": "Maison des jeunes L'Antidote de Duberger - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 191
  },
  {
    "Location": "Odyssey I - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 190
  },
  {
    "Location": "Boys and Girls Clubs of Winnipeg Inc. - Main Club",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 190
  },
  {
    "Location": "Durham College  - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 189
  },
  {
    "Location": "Falther Don McLellan Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 189
  },
  {
    "Location": "Boys and Girls Club of Wetaskiwin - Main Club",
    "Club": "Boys and Girls Club of Wetaskiwin",
    "Total time offline in mins": 189
  },
  {
    "Location": "Hudson Road After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 189
  },
  {
    "Location": "Vernon Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 189
  },
  {
    "Location": "Delburne - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 188
  },
  {
    "Location": "Ralph Thornton Centre - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 188
  },
  {
    "Location": "Sheppard Africentric Alternative School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 188
  },
  {
    "Location": "Anderson CVI - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 187
  },
  {
    "Location": "Parents Together - Ray-Cam Co-operative Centre - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 187
  },
  {
    "Location": "Boys and Girls Clubs of Whitecourt & District - Main Club",
    "Club": "Boys and Girls Clubs of Whitecourt & District",
    "Total time offline in mins": 187
  },
  {
    "Location": "Maison Coup De Pouce T.R. - Main Club",
    "Club": "Maison Coup De Pouce T.R.",
    "Total time offline in mins": 187
  },
  {
    "Location": "Sanford Boys and Girls Club - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 186
  },
  {
    "Location": "Skills Link - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 185
  },
  {
    "Location": "Valleyfield Junior School - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 185
  },
  {
    "Location": "Club Francophone  - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 184
  },
  {
    "Location": "Bert Edwards Science and Technology School - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 184
  },
  {
    "Location": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area - Main Club",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 184
  },
  {
    "Location": "Boys and Girls Club of Lethbridge & District - Main Club",
    "Club": "Boys and Girls Club of Lethbridge & District",
    "Total time offline in mins": 183
  },
  {
    "Location": "L'Alternatif de la Ribambelle - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 183
  },
  {
    "Location": "Forest Park Club - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 182
  },
  {
    "Location": "Vincent Massey Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 182
  },
  {
    "Location": "Chase River Club - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 181
  },
  {
    "Location": "Sinclair Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 180
  },
  {
    "Location": "Maison des jeunes de Neuville - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 180
  },
  {
    "Location": "Legends Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 179
  },
  {
    "Location": "Thorncliffe Club - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 179
  },
  {
    "Location": "Scarborough East Ontario Early Years Centre - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 177
  },
  {
    "Location": "Family Centre White Oaks - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 177
  },
  {
    "Location": "Oyama Traditional School - After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 177
  },
  {
    "Location": "Madonna Catholic Elementary School - Service Location",
    "Club": "Boys & Girls Club of Strathcona County",
    "Total time offline in mins": 175
  },
  {
    "Location": "Armstrong Community Centre / Office - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 175
  },
  {
    "Location": "Holy Trinity School  - Service Location",
    "Club": "Boys & Girls Club of Olds & Area",
    "Total time offline in mins": 174
  },
  {
    "Location": "Crowsnest Community Library - Service Location",
    "Club": "Boys and Girls Club of Crowsnest Pass",
    "Total time offline in mins": 174
  },
  {
    "Location": "Camp Alexo - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 174
  },
  {
    "Location": "Coal Tyee Elementary - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 174
  },
  {
    "Location": "St Alphonsus Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 174
  },
  {
    "Location": "L'Entre-Ados - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 174
  },
  {
    "Location": "Silverspring BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 173
  },
  {
    "Location": "Ontario Early Years Centre Summer Camp  - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 172
  },
  {
    "Location": "Pilier jeunesse - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 172
  },
  {
    "Location": "Drayton Valley - Service Location",
    "Club": "Boys and Girls Club of Wetaskiwin",
    "Total time offline in mins": 171
  },
  {
    "Location": "Rado - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 171
  },
  {
    "Location": "Bridgewood Public School - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 170
  },
  {
    "Location": "Esquimalt Club - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 170
  },
  {
    "Location": "St. Stephen High School - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 168
  },
  {
    "Location": "Wellwood - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 168
  },
  {
    "Location": "Boys and Girls Club of Truro and Colchester - Main Club",
    "Club": "Boys and Girls Club of Truro and Colchester",
    "Total time offline in mins": 167
  },
  {
    "Location": "Discovery Public School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 167
  },
  {
    "Location": "Boys and Girls Clubs of Kawartha Lakes - Main Club",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 167
  },
  {
    "Location": "Sir William Stephenson Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 166
  },
  {
    "Location": "East Scarborough Childcare Centre - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 166
  },
  {
    "Location": "HOPE Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 166
  },
  {
    "Location": "Boys and Girls Club of Ottawa - Main Club",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 166
  },
  {
    "Location": "Rutland Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 166
  },
  {
    "Location": "The Range (Program/Office Space) - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 165
  },
  {
    "Location": "Fort McMurray Boys and Girls Club - Main Club",
    "Club": "Fort McMurray Boys and Girls Club",
    "Total time offline in mins": 165
  },
  {
    "Location": "Maison des jeunes du quartier St-Jean-Baptiste - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 165
  },
  {
    "Location": "Fifth Street Club - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 164
  },
  {
    "Location": "Lantzville Club - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 164
  },
  {
    "Location": "Martin Avenue Community Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 164
  },
  {
    "Location": "Point de service St-Tite-des-Caps - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 164
  },
  {
    "Location": "Glen Park Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 164
  },
  {
    "Location": "University of Toronto - Scarborough Campus - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 163
  },
  {
    "Location": "Boys and Girls Clubs of Dawson - Main Club",
    "Club": "Boys and Girls Clubs of Dawson",
    "Total time offline in mins": 163
  },
  {
    "Location": "Youth Mentorship Program - YMCA Immigrant Services - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 162
  },
  {
    "Location": "St. Brendan Afterschool Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 162
  },
  {
    "Location": "Thorold Satellite At Ontario Street Public School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 162
  },
  {
    "Location": "Police Youth Centre - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 162
  },
  {
    "Location": "Niagara Falls Centre (Main Club Site) - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 161
  },
  {
    "Location": "Prairie View Elementary BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 161
  },
  {
    "Location": "Petitcodiac Boys and Girls Club Inc. - Main Club",
    "Club": "Petitcodiac Boys and Girls Club Inc.",
    "Total time offline in mins": 161
  },
  {
    "Location": "Bala Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 161
  },
  {
    "Location": "Eastdale CVI-Oshawa - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 160
  },
  {
    "Location": "Heatherington Community Centre - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 160
  },
  {
    "Location": "Grandravine Children's Programs TCHC - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 160
  },
  {
    "Location": "Toronto Kiwanis Boys and Girls Clubs - Main Club",
    "Club": "Toronto Kiwanis Boys and Girls Clubs",
    "Total time offline in mins": 160
  },
  {
    "Location": "Boys & Girls Club of Charlotte County - Main Club",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 159
  },
  {
    "Location": "Boys and Girls Club of Durham - Main Club",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 159
  },
  {
    "Location": "J. Clarke Richardson/Notre Dame S.S. - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 159
  },
  {
    "Location": "Camp Adventure - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 159
  },
  {
    "Location": "Chester Elementary School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 159
  },
  {
    "Location": "R.J. Hawkey School - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 158
  },
  {
    "Location": "Parent Services - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 158
  },
  {
    "Location": "Port Perry Library - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 157
  },
  {
    "Location": "Monsignor Percy Johnson Catholic School - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 156
  },
  {
    "Location": "Boys & Girls Club of Moncton - Main Club",
    "Club": "Boys & Girls Club of Moncton",
    "Total time offline in mins": 156
  },
  {
    "Location": "Dawe Comunity Programs - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 156
  },
  {
    "Location": "St. Helens Separate School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 156
  },
  {
    "Location": "Nose Creek Elementary School - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 155
  },
  {
    "Location": "Main Administration Office - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 155
  },
  {
    "Location": "Boys and Girls Clubs of Cape Breton-Whitney Pier Youth Club - Main Club",
    "Club": "Boys and Girls Clubs of Cape Breton-Whitney Pier Youth Club",
    "Total time offline in mins": 155
  },
  {
    "Location": "Ladysmith Club - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 155
  },
  {
    "Location": "All Saints Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 154
  },
  {
    "Location": "Kinsmen Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 154
  },
  {
    "Location": "Parents Together - South Asian Group - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 154
  },
  {
    "Location": "St Alban's Main Club Site - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 154
  },
  {
    "Location": "Boys & Girls Club of Strathcona County - Main Club",
    "Club": "Boys & Girls Club of Strathcona County",
    "Total time offline in mins": 153
  },
  {
    "Location": "Oshawa Library Main Branch - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 153
  },
  {
    "Location": "St. Mary's of the Lake School - Service Location",
    "Club": "Boys and Girls Club of Slave Lake",
    "Total time offline in mins": 153
  },
  {
    "Location": "Ontario Early Years Centre- Sanford Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 153
  },
  {
    "Location": "St. Michael Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 153
  },
  {
    "Location": "TKBGC Main Club Site & Miles & Kelly Nadal Youth Centre - Service Location",
    "Club": "Toronto Kiwanis Boys and Girls Clubs",
    "Total time offline in mins": 153
  },
  {
    "Location": "Brooklyn Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 152
  },
  {
    "Location": "Nexus - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 152
  },
  {
    "Location": "Lincoln Ave Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 151
  },
  {
    "Location": "Norwood - Service Location",
    "Club": "Boys and Girls Club of Wetaskiwin",
    "Total time offline in mins": 151
  },
  {
    "Location": "Terry Fox Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 150
  },
  {
    "Location": "Gibson Neil Memorial Elementary School - Service Location",
    "Club": "Boys and Girls Club of Fredericton",
    "Total time offline in mins": 150
  },
  {
    "Location": "Satellite Location - Service Location",
    "Club": "Boys and Girls Club of Lethbridge & District",
    "Total time offline in mins": 150
  },
  {
    "Location": "South Delta Family Resource Centre - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 150
  },
  {
    "Location": "Armstrong Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 150
  },
  {
    "Location": "OK Falls Community Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 150
  },
  {
    "Location": "Maison des jeunes de Charlesbourg (L'Intégrale) - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 150
  },
  {
    "Location": "Let's Get Moving- Queen Mary School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 149
  },
  {
    "Location": "Club Garçons et Filles - Local des jeunes des Jardins Fleuris - Main Club",
    "Club": "Club Garçons et Filles - Local des jeunes des Jardins Fleuris",
    "Total time offline in mins": 148
  },
  {
    "Location": "Boys and Girls Club of Irricana  - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 147
  },
  {
    "Location": "The Elms Junior Middle School - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 147
  },
  {
    "Location": "Pelham TCHC - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 147
  },
  {
    "Location": "North Hill Club - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 146
  },
  {
    "Location": "Falkland Elementary School - After School Recreation Programs - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 146
  },
  {
    "Location": "St. Alban's Boys and Girls Club - Main Club",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 146
  },
  {
    "Location": "506 Clubhouse - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 145
  },
  {
    "Location": "John Lake BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 145
  },
  {
    "Location": "L'Intégrale des Thuyas - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 145
  },
  {
    "Location": "Carruthers Creek Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 144
  },
  {
    "Location": "Lakeridge Health Oshawa - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 144
  },
  {
    "Location": "Willowgrove BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 144
  },
  {
    "Location": "North Albion Collegiate Institute - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 142
  },
  {
    "Location": "Carea Community Health Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 142
  },
  {
    "Location": "Brampton Centennial S. S. - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 142
  },
  {
    "Location": "The Boys and Girls Before and After School Care - Service Location",
    "Club": "Boys and Girls Club of St. Paul & District",
    "Total time offline in mins": 142
  },
  {
    "Location": "Kids in Motion Licensed Child Care At the Kawartha Lakes Club - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 142
  },
  {
    "Location": "Courtice Recreation Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 141
  },
  {
    "Location": "White Oaks - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 141
  },
  {
    "Location": "Glass Slippers - Service Location",
    "Club": "Boys and Girls Club of Williams Lake and District",
    "Total time offline in mins": 141
  },
  {
    "Location": "North Simcoe Sports and Recreation Centre - Service Location",
    "Club": "Boys and Girls Clubs of North Simcoe",
    "Total time offline in mins": 141
  },
  {
    "Location": "Building Blocks Daycare - Service Location",
    "Club": "Cranbrook Boys and Girls Club",
    "Total time offline in mins": 141
  },
  {
    "Location": "Main Clubhouse - Service Location",
    "Club": "Boys and Girls Club of Pembroke",
    "Total time offline in mins": 140
  },
  {
    "Location": "NGEN Youth Centre - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 140
  },
  {
    "Location": "Peachland Elementary Preschool Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 140
  },
  {
    "Location": "Centre For Individual Studies-Bowmanville - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 139
  },
  {
    "Location": "Skyline Facility - Skyline Recreation Centre - Service Location",
    "Club": "Boys and Girls Club of Fredericton",
    "Total time offline in mins": 139
  },
  {
    "Location": "Dalhousie Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 139
  },
  {
    "Location": "Vimey Ridge Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 138
  },
  {
    "Location": "Hillsborough Youth Centre - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 138
  },
  {
    "Location": "Confederation Park Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 138
  },
  {
    "Location": "Victor Mager Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 138
  },
  {
    "Location": "Maison des jeunes de Pont-Rouge - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 138
  },
  {
    "Location": "Northbrae Public School - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 137
  },
  {
    "Location": "Outdoor Centre - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 137
  },
  {
    "Location": "McCauley Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 137
  },
  {
    "Location": "Boys and Girls Clubs of North Simcoe - Main Club",
    "Club": "Boys and Girls Clubs of North Simcoe",
    "Total time offline in mins": 137
  },
  {
    "Location": "St. John Bosco Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 137
  },
  {
    "Location": "Maison des jeunes de Beauport - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 137
  },
  {
    "Location": "Beattie Elementary - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 136
  },
  {
    "Location": "Wesley Community Church - Service Location",
    "Club": "Boys and Girls Club of Pembroke",
    "Total time offline in mins": 136
  },
  {
    "Location": "Park Avenue Public School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 136
  },
  {
    "Location": "Hugh Cairns BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 136
  },
  {
    "Location": "Earl Grey Senior Public School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 136
  },
  {
    "Location": "George Pringle After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 136
  },
  {
    "Location": "The Boys and Girls Club of Grand Manan Island Inc. - Main Club",
    "Club": "The Boys and Girls Club of Grand Manan Island Inc.",
    "Total time offline in mins": 136
  },
  {
    "Location": "St.Pius X School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 135
  },
  {
    "Location": "Boys and Girls Club of Pembroke - Main Club",
    "Club": "Boys and Girls Club of Pembroke",
    "Total time offline in mins": 134
  },
  {
    "Location": "Clairville Junior School - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 133
  },
  {
    "Location": "Port Colborne Satellite At McKay Public School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 133
  },
  {
    "Location": "Agincourt Ontario Early Years Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 133
  },
  {
    "Location": "Aspen Park Elementary - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 133
  },
  {
    "Location": "C.E. Webster Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 133
  },
  {
    "Location": "Bright Adventures Daycare - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 132
  },
  {
    "Location": "Star of the Sea - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 132
  },
  {
    "Location": "Pearson After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 132
  },
  {
    "Location": "Boys & Girls Club of Thompson Inc. - Main Club",
    "Club": "Boys & Girls Club of Thompson Inc.",
    "Total time offline in mins": 131
  },
  {
    "Location": "Beban House - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 131
  },
  {
    "Location": "Work BC Delta - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 131
  },
  {
    "Location": "Miramichi Boys and Girls Club - Main Club",
    "Club": "Miramichi Boys and Girls Club",
    "Total time offline in mins": 131
  },
  {
    "Location": "L'Alibi de Cambert - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 131
  },
  {
    "Location": "Camp Smitty - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 130
  },
  {
    "Location": "Boys and Girls Club of Yorkton Inc. - Main Club",
    "Club": "Boys and Girls Club of Yorkton Inc.",
    "Total time offline in mins": 130
  },
  {
    "Location": "Edson District Boys and Girls Club - Service Location",
    "Club": "Edson and District Boys and Girls Club",
    "Total time offline in mins": 130
  },
  {
    "Location": "Boys and Girls Club of Summerside Inc. - Main Club",
    "Club": "Boys and Girls Club of Summerside Inc.",
    "Total time offline in mins": 129
  },
  {
    "Location": "Beacon United Church - Service Location",
    "Club": "Boys and Girls Club of Yarmouth",
    "Total time offline in mins": 129
  },
  {
    "Location": "Marvin Heights Public School - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 128
  },
  {
    "Location": "Glengrove Public School  - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 127
  },
  {
    "Location": "Colonial Terrace - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 126
  },
  {
    "Location": "Robert B. Colborne Building - Service Location",
    "Club": "Boys and Girls Club of Wetaskiwin",
    "Total time offline in mins": 126
  },
  {
    "Location": "St. Paul BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 126
  },
  {
    "Location": "Westside Youth Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 125
  },
  {
    "Location": "Maison des jeunes de Limoilou - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 124
  },
  {
    "Location": "Thistletown Collegiate Institute - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 123
  },
  {
    "Location": "The Boys and Girls Club of Saint John Inc. - Main Club",
    "Club": "The Boys and Girls Club of Saint John Inc.",
    "Total time offline in mins": 122
  },
  {
    "Location": "Boys and Girls Club of Charlottetown - Main Club",
    "Club": "Boys and Girls Club of Charlottetown",
    "Total time offline in mins": 121
  },
  {
    "Location": "Child - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 121
  },
  {
    "Location": "Maison des jeunes la Baraque des Éboulements - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 121
  },
  {
    "Location": "Boys and Girls Club of Airdrie - Main Club",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 120
  },
  {
    "Location": "Brunskill BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 120
  },
  {
    "Location": "Alexander Muir Gladstone Ave PS - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 120
  },
  {
    "Location": "Humber Park - Service Location",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 119
  },
  {
    "Location": "Kiwanis Youth Centre for Sports Excellence - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 119
  },
  {
    "Location": "Kimount Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 119
  },
  {
    "Location": "Youth Mentorship Program - PJ Secondary - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 118
  },
  {
    "Location": "Donald A. Wilson SS - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 116
  },
  {
    "Location": "John Lake Preschool - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 115
  },
  {
    "Location": "The Centre - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 114
  },
  {
    "Location": "St. Edward BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 114
  },
  {
    "Location": "Maison des jeunes de Neufchâtel (La Clique) - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 114
  },
  {
    "Location": "Whitby Public Library - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 113
  },
  {
    "Location": "Holy Family Catholic School - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 113
  },
  {
    "Location": "Maison des jeunes de l'Ile d'Orléans - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 113
  },
  {
    "Location": "West Scarborough RRTG Location - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 111
  },
  {
    "Location": "Driftwood Court TCHC - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 111
  },
  {
    "Location": "Hangar Club / South Clubs (Calgary After School) - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 109
  },
  {
    "Location": "St. Bruno Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 109
  },
  {
    "Location": "Murray McKinnon House - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 107
  },
  {
    "Location": "Vic West Community Club - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 107
  },
  {
    "Location": "Buckmaster's Circle Unit - Service Location",
    "Club": "Boys and Girls Clubs of St. John's",
    "Total time offline in mins": 106
  },
  {
    "Location": "T.P. Loblaw Site at St. Mary Catholic School - Service Location",
    "Club": "Toronto Kiwanis Boys and Girls Clubs",
    "Total time offline in mins": 106
  },
  {
    "Location": "Boys and Girls Club of Slave Lake - Main Club",
    "Club": "Boys and Girls Club of Slave Lake",
    "Total time offline in mins": 105
  },
  {
    "Location": "Gosford Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 105
  },
  {
    "Location": "West Hill After School Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 104
  },
  {
    "Location": "Leduc service location* - Service Location",
    "Club": "Boys and Girls Club of Leduc",
    "Total time offline in mins": 104
  },
  {
    "Location": "Summer in the City Day Camp West - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 104
  },
  {
    "Location": "Maison des jeunes de Charlesbourg (La Marginale) - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 104
  },
  {
    "Location": "St. Thomas Aquinas Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 103
  },
  {
    "Location": "Gladstone Public - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 102
  },
  {
    "Location": "Muslim Shelter - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 102
  },
  {
    "Location": "Ontario Early Years Centre- Congress Neighbourhood Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 102
  },
  {
    "Location": "Youth and Family Services and Sexual Abuse Intervention Program - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 102
  },
  {
    "Location": "Penticton Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 102
  },
  {
    "Location": "Cole Harbour - Service Location",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 101
  },
  {
    "Location": "John Dryden Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 101
  },
  {
    "Location": "Davidson Road Elementary School - After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 100
  },
  {
    "Location": "Penny Lane Transition House - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 100
  },
  {
    "Location": "Maxwell Heights Secondary School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 99
  },
  {
    "Location": "Seaview After School - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 99
  },
  {
    "Location": "Kensingston Community School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 99
  },
  {
    "Location": "Petitcodiac Youth Culture House - Service Location",
    "Club": "Petitcodiac Boys and Girls Club Inc.",
    "Total time offline in mins": 98
  },
  {
    "Location": "Chief Tomat Preschool - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 97
  },
  {
    "Location": "Courtice Secondary School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 96
  },
  {
    "Location": "Champlain Discovery School - Service Location",
    "Club": "Boys and Girls Club of Pembroke",
    "Total time offline in mins": 96
  },
  {
    "Location": "Clearwater Boys and Girls Club - Main Club",
    "Club": "Clearwater Boys and Girls Club",
    "Total time offline in mins": 96
  },
  {
    "Location": "Firgrove Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 96
  },
  {
    "Location": "Rideau Heights Public School - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 95
  },
  {
    "Location": "A.E. Perry Elementary School - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 94
  },
  {
    "Location": "Richmond Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 94
  },
  {
    "Location": "McMurrich Junior Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 94
  },
  {
    "Location": "Major Ballachey After School Program - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 93
  },
  {
    "Location": "Harold Longworth Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 93
  },
  {
    "Location": "Early Learning & Child Care Centre  -- Ellis Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 93
  },
  {
    "Location": "Perth Avenue Public School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 93
  },
  {
    "Location": "Kids First Child Care At St Gabriel Lalemant Catholic Elementary School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 92
  },
  {
    "Location": "Sir James Dunn Academy - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 91
  },
  {
    "Location": "St. Columban's Catholic School - Service Location",
    "Club": "Boys & Girls Club of Cornwall",
    "Total time offline in mins": 91
  },
  {
    "Location": "Pike Lake Summer Day Camp - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 91
  },
  {
    "Location": "Miramichi - Service Location",
    "Club": "Miramichi Boys and Girls Club",
    "Total time offline in mins": 91
  },
  {
    "Location": "Main Office - Service Location",
    "Club": "Boys and Girls Club of Cochrane and Area",
    "Total time offline in mins": 89
  },
  {
    "Location": "Buena Vista BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 89
  },
  {
    "Location": "Cranbrook Boys and Girls Club - Main Club",
    "Club": "Cranbrook Boys and Girls Club",
    "Total time offline in mins": 89
  },
  {
    "Location": "Dieppe Boys and Girls Club Inc. - Main Club",
    "Club": "Dieppe Boys and Girls Club Inc.",
    "Total time offline in mins": 89
  },
  {
    "Location": "MDJ St-Aimé-des-Lacs - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 89
  },
  {
    "Location": "Creditvale Mills - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 88
  },
  {
    "Location": "Henry Kelsey BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 88
  },
  {
    "Location": "Windsor Unit - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 88
  },
  {
    "Location": "Alexis Park Elementary School - After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 88
  },
  {
    "Location": "Eastside Childcare Centre - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 87
  },
  {
    "Location": "Piitoyais Family School - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 87
  },
  {
    "Location": "Parents Together - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 87
  },
  {
    "Location": "Aberdeen Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 87
  },
  {
    "Location": "L'Amoreaux Community Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 86
  },
  {
    "Location": "John-Rennie High School  - Service Location",
    "Club": "Boys and Girls Clubs of Dawson",
    "Total time offline in mins": 86
  },
  {
    "Location": "McQuesten Boys and Girls Club - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 86
  },
  {
    "Location": "Sakaw Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 85
  },
  {
    "Location": "EMBM Afterschool Program - Service Location",
    "Club": "Battlefords Boys and Girls Club",
    "Total time offline in mins": 84
  },
  {
    "Location": "Eastview Unit - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 84
  },
  {
    "Location": "Millstream Club - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 84
  },
  {
    "Location": "Loblaws-The East Mall - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 84
  },
  {
    "Location": "Springvalley After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 84
  },
  {
    "Location": "Spryfield - Service Location",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 83
  },
  {
    "Location": "Phoebe Gilman Public School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 83
  },
  {
    "Location": "West End Hub (BGC Kingston) - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 82
  },
  {
    "Location": "Ontario Works Social Services - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 81
  },
  {
    "Location": "Dunsford Club At Dunsford District Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 81
  },
  {
    "Location": "Boys and Girls Clubs of the Foothills - Main Club",
    "Club": "Boys and Girls Clubs of the Foothills",
    "Total time offline in mins": 81
  },
  {
    "Location": "Boys and Girls Club of Kingston & Area Inc. - Main Club",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 80
  },
  {
    "Location": "Frank L. Bowser - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 80
  },
  {
    "Location": "St. Peter BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 80
  },
  {
    "Location": "St. Stephens Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 79
  },
  {
    "Location": "Oriole Boys & Girls Club - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 79
  },
  {
    "Location": "Westwood Middle School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 79
  },
  {
    "Location": "Osoyoos Youth Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 79
  },
  {
    "Location": "Dante Alighieri Catholic High School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 79
  },
  {
    "Location": "Chippewa Satellite At Riverview Public School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 78
  },
  {
    "Location": "Norvan Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 78
  },
  {
    "Location": "Holy Child Catholic School - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 78
  },
  {
    "Location": "Helen Gorman Preschool - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 78
  },
  {
    "Location": "Humber TCHC - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 78
  },
  {
    "Location": "Boys & Girls Club of Montague - Service Location",
    "Club": "Boys and Girls Club of Charlottetown",
    "Total time offline in mins": 77
  },
  {
    "Location": "Work BC Delta - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 75
  },
  {
    "Location": "Westview High School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 75
  },
  {
    "Location": "Let's Get Moving- C.B. Stirling School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 74
  },
  {
    "Location": "Boys and Girls Club of East Scarborough - Main Club",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 72
  },
  {
    "Location": "Maple Leaf Public School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 72
  },
  {
    "Location": "Westshore Club - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 72
  },
  {
    "Location": "HLM Place-de-la-Rive - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 72
  },
  {
    "Location": "Pelham Satellite At A.K. Wiggs Public School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 71
  },
  {
    "Location": "The Bridge (Office Space) - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 71
  },
  {
    "Location": "Boys and Girls Clubs of Bashaw & Area - Main Club",
    "Club": "Boys and Girls Clubs of Bashaw & Area",
    "Total time offline in mins": 70
  },
  {
    "Location": "Norquay Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 70
  },
  {
    "Location": "Edson and District Boys and Girls Club - Main Club",
    "Club": "Edson and District Boys and Girls Club",
    "Total time offline in mins": 70
  },
  {
    "Location": "Clarington Central High School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 69
  },
  {
    "Location": "Devon Facility - Henry Park Recreation Centre - Service Location",
    "Club": "Boys and Girls Club of Fredericton",
    "Total time offline in mins": 68
  },
  {
    "Location": "Fort Erie Centre - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 68
  },
  {
    "Location": "John Stubbs School - Service Location",
    "Club": "Boys and Girls Club Services of Greater Victoria",
    "Total time offline in mins": 68
  },
  {
    "Location": "Spruce View - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 67
  },
  {
    "Location": "Let's Get Moving- St. Ann School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 67
  },
  {
    "Location": "Boys and Girls Club of Whitecourt District - Service Location",
    "Club": "Boys and Girls Clubs of Whitecourt & District",
    "Total time offline in mins": 67
  },
  {
    "Location": "Gander Boys and Girls Club - Main Club",
    "Club": "Gander Boys and Girls Club",
    "Total time offline in mins": 67
  },
  {
    "Location": "Nightlife Youth Services - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 66
  },
  {
    "Location": "West Scarborough Neighbourhood Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 66
  },
  {
    "Location": "Caroline Robins BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 65
  },
  {
    "Location": "Saskatoon French BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 65
  },
  {
    "Location": "Maison des jeunes de Stoneham - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 65
  },
  {
    "Location": "Brooklin Community Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 64
  },
  {
    "Location": "St. Pauls Catholic School Site - Service Location",
    "Club": "Toronto Kiwanis Boys and Girls Clubs",
    "Total time offline in mins": 64
  },
  {
    "Location": "Bowmanville Library - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 63
  },
  {
    "Location": "Maison des jeunes de Vanier - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 63
  },
  {
    "Location": "Glamorgan Public School - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 62
  },
  {
    "Location": "Eastview Neighbourhood Community Centre - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 62
  },
  {
    "Location": "Corvette Family Resource Centre - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 61
  },
  {
    "Location": "White Buffalo Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 61
  },
  {
    "Location": "Peachland Boys and Girls Club - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 61
  },
  {
    "Location": "Youth Mentorship Program - Eagle Place - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 60
  },
  {
    "Location": "Hillside Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 60
  },
  {
    "Location": "Port Union Library - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 59
  },
  {
    "Location": "Let's Get Moving- Prince of Wales School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 59
  },
  {
    "Location": "St Matthews Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 59
  },
  {
    "Location": "Woolner TCHC - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 59
  },
  {
    "Location": "James Lyng High School - Service Location",
    "Club": "Boys and Girls Clubs of Dawson",
    "Total time offline in mins": 58
  },
  {
    "Location": "Tot Spot - Service Location",
    "Club": "Boys and Girls Club of Yorkton Inc.",
    "Total time offline in mins": 57
  },
  {
    "Location": "Downtown Youth Centre - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 57
  },
  {
    "Location": "Heather Heights Junior Public School - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 55
  },
  {
    "Location": "Peter Greer Elementary School - After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 55
  },
  {
    "Location": "Boys & Girls Clubs of Greater Halifax - Main Club",
    "Club": "Boys & Girls Clubs of Greater Halifax",
    "Total time offline in mins": 54
  },
  {
    "Location": "Durham Alternative Secondary School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 54
  },
  {
    "Location": "Welland Satellite At Ross Public School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 54
  },
  {
    "Location": "Stephen Leacock Community Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 54
  },
  {
    "Location": "Early Learning Centre - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 54
  },
  {
    "Location": "Claude D. Taylor School - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 53
  },
  {
    "Location": "Wellington & Area Boys and Girls Club - Main Club",
    "Club": "Wellington & Area Boys and Girls Club",
    "Total time offline in mins": 53
  },
  {
    "Location": "Fundy High School - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 52
  },
  {
    "Location": "Bowness Club - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 52
  },
  {
    "Location": "Claude E Garton Public School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 52
  },
  {
    "Location": "Repaire jeunesse de Sherbrooke – Ascot - Main Club",
    "Club": "Repaire jeunesse de Sherbrooke – Ascot",
    "Total time offline in mins": 52
  },
  {
    "Location": "St. John the Evangelist Catholic School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 51
  },
  {
    "Location": "South West Ontario Early Years Centre - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 51
  },
  {
    "Location": "Blake Street Junior Public School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 51
  },
  {
    "Location": "Regal Road Junior Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 51
  },
  {
    "Location": "O'Neill CVI - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 49
  },
  {
    "Location": "Robert Meek Youth Centre - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 49
  },
  {
    "Location": "Mundy Pond Unit - Service Location",
    "Club": "Boys and Girls Clubs of St. John's",
    "Total time offline in mins": 49
  },
  {
    "Location": "Greenholme Jr. School - Service Location",
    "Club": "Albion Neighbourhood Services Boys and Girls Club",
    "Total time offline in mins": 48
  },
  {
    "Location": "Newcastle Community Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 48
  },
  {
    "Location": "NSCC Bumidge Campus - Service Location",
    "Club": "Boys and Girls Club of Yarmouth",
    "Total time offline in mins": 48
  },
  {
    "Location": "Parenting afterSeparation - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 47
  },
  {
    "Location": "Driftwood Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 47
  },
  {
    "Location": "South End Community Centre - Service Location",
    "Club": "The Boys and Girls Club of Saint John Inc.",
    "Total time offline in mins": 47
  },
  {
    "Location": "Beltline Youth Centre - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 46
  },
  {
    "Location": "Corpus Christi Catholic Elementary School - Service Location",
    "Club": "Boys and Girls Clubs of Thunder Bay",
    "Total time offline in mins": 46
  },
  {
    "Location": "Boys and Girls Club of Bonnyville - Main Club",
    "Club": "Boys and Girls Club of Bonnyville",
    "Total time offline in mins": 45
  },
  {
    "Location": "Queen Elizabeth Centre - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 45
  },
  {
    "Location": "St. Goretti Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 44
  },
  {
    "Location": "St. Mary School - Service Location",
    "Club": "Boys and Girls Clubs of Whitecourt & District",
    "Total time offline in mins": 44
  },
  {
    "Location": "Boys and Girls Club of Midland - Service Location",
    "Club": "Boys and Girls Clubs of North Simcoe",
    "Total time offline in mins": 43
  },
  {
    "Location": "St-Hilarion - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 43
  },
  {
    "Location": "Boys and Girls Club of Fort Saskatchewan - Main Club",
    "Club": "Boys and Girls Club of Fort Saskatchewan",
    "Total time offline in mins": 42
  },
  {
    "Location": "Columbia School - Service Location",
    "Club": "Boys and Girls Club of Yorkton Inc.",
    "Total time offline in mins": 42
  },
  {
    "Location": "St. Mary's School - Service Location",
    "Club": "Boys and Girls Club of Yorkton Inc.",
    "Total time offline in mins": 42
  },
  {
    "Location": "Bready Elementary Program - Service Location",
    "Club": "Battlefords Boys and Girls Club",
    "Total time offline in mins": 41
  },
  {
    "Location": "John Graves Simcoe Public School - Service Location",
    "Club": "Boys and Girls Club of Kingston & Area Inc.",
    "Total time offline in mins": 40
  },
  {
    "Location": "St. Augustine BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 40
  },
  {
    "Location": "Wabana Boys and Girls Club - Main Club",
    "Club": "Wabana Boys and Girls Club",
    "Total time offline in mins": 40
  },
  {
    "Location": "Hera - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 39
  },
  {
    "Location": "Kivan Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 39
  },
  {
    "Location": "Boys and Girls Clubs of Yukon - Main Club",
    "Club": "Boys and Girls Clubs of Yukon",
    "Total time offline in mins": 39
  },
  {
    "Location": "Boys and Girls Club of Rimbey - Service Location",
    "Club": "Boys & Girls Club of Wolf Creek - Ponoka",
    "Total time offline in mins": 38
  },
  {
    "Location": "Stevensville Satellite At St. Joseph Catholic School - Service Location",
    "Club": "Boys and Girls Club of Niagara",
    "Total time offline in mins": 38
  },
  {
    "Location": "The Deck (Program and Office Space) - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 38
  },
  {
    "Location": "St. George BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 38
  },
  {
    "Location": "South Rutland After School Program - Service Location",
    "Club": "Okanagan Boys & Girls Clubs",
    "Total time offline in mins": 38
  },
  {
    "Location": "Oakdale Community Centre - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 38
  },
  {
    "Location": "R.S. McLaughlin CVI - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 37
  },
  {
    "Location": "West Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 37
  },
  {
    "Location": "Georges Vanier BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 37
  },
  {
    "Location": "Ridgemont High School - Service Location",
    "Club": "Boys and Girls Club of Ottawa",
    "Total time offline in mins": 35
  },
  {
    "Location": "Boys and Girls Club of Riverview - Main Club",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 35
  },
  {
    "Location": "Mother Teresa BASP - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 35
  },
  {
    "Location": "Bolton C.Falby Public School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 34
  },
  {
    "Location": "Bowden Keystone Club - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 32
  },
  {
    "Location": "Penhold - Service Location",
    "Club": "Boys and Girls Club of Red Deer and District",
    "Total time offline in mins": 32
  },
  {
    "Location": "Wilkinson Public School - Service Location",
    "Club": "Eastview (Toronto) Boys and Girls Club",
    "Total time offline in mins": 31
  },
  {
    "Location": "Parents Together - Vietnamese Group - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 30
  },
  {
    "Location": "Sister MacNamara Club - Service Location",
    "Club": "Boys and Girls Clubs of Winnipeg Inc.",
    "Total time offline in mins": 30
  },
  {
    "Location": "St Jean de Brebeuf Catholic School - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 29
  },
  {
    "Location": "Boys and Girls Club of London - Main Club",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 29
  },
  {
    "Location": "Acorn Place - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 28
  },
  {
    "Location": "Coboconk Club at Ridgewood Public School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 28
  },
  {
    "Location": "Fraserview Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 28
  },
  {
    "Location": "Mornelle Family Resource Centre - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 27
  },
  {
    "Location": "Early Learning & Child Care Centre -- Queen Mary Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 27
  },
  {
    "Location": "Battlefords Boys and Girls Club - Main Club",
    "Club": "Battlefords Boys and Girls Club",
    "Total time offline in mins": 26
  },
  {
    "Location": "George B Little After School Program - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 26
  },
  {
    "Location": "Family Centre Argyle - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 26
  },
  {
    "Location": "Petitcodiac Regional School - Service Location",
    "Club": "Petitcodiac Boys and Girls Club Inc.",
    "Total time offline in mins": 26
  },
  {
    "Location": "L'Aventurier de Montmorency - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 26
  },
  {
    "Location": "Stanley Public School - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 26
  },
  {
    "Location": "Woodbridge Farms Elementary School - Service Location",
    "Club": "Boys & Girls Club of Strathcona County",
    "Total time offline in mins": 25
  },
  {
    "Location": "Firehouse Youth Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 24
  },
  {
    "Location": "Northview Community Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 24
  },
  {
    "Location": "Comox Valley Administration - Service Location",
    "Club": "Boys and Girls Clubs of Central Vancouver Island",
    "Total time offline in mins": 23
  },
  {
    "Location": "Saddle Lake Boys and Girls Club - Main Club",
    "Club": "Saddle Lake Boys and Girls Club",
    "Total time offline in mins": 23
  },
  {
    "Location": "Georgina Island First Nations Reserve - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 22
  },
  {
    "Location": "Forest Lawn High School - Wellness Centre - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 22
  },
  {
    "Location": "Action Jeunesse St-Pie X de Longueuil - Main Club",
    "Club": "Action Jeunesse St-Pie X de Longueuil",
    "Total time offline in mins": 21
  },
  {
    "Location": "Let's Get Moving- Holy Name of Jesus School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 21
  },
  {
    "Location": "Forum Jeunesse Charlevoix Ouest - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 21
  },
  {
    "Location": "Botwood Boys and Girls Club Inc. - Main Club",
    "Club": "Botwood Boys and Girls Club Inc.",
    "Total time offline in mins": 20
  },
  {
    "Location": "Abilities Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 20
  },
  {
    "Location": "Robert Service Senior Public School - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 20
  },
  {
    "Location": "Secord Public School - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 20
  },
  {
    "Location": "Tweddle Place Club - Service Location",
    "Club": "Boys and Girls Clubs Big Brothers Big Sisters of Edmonton & Area",
    "Total time offline in mins": 20
  },
  {
    "Location": "Pleasant Hill Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 20
  },
  {
    "Location": "Dundas Junior Public School - Service Location",
    "Club": "Toronto Kiwanis Boys and Girls Clubs",
    "Total time offline in mins": 20
  },
  {
    "Location": "Upper Island Cove Boys and Girls Club - Main Club",
    "Club": "Upper Island Cove Boys and Girls Club",
    "Total time offline in mins": 19
  },
  {
    "Location": "Boys and Girls Club of Kamloops - Main Club",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 18
  },
  {
    "Location": "Sir William Osler High School - Service Location",
    "Club": "Boys and Girls Club of West Scarborough",
    "Total time offline in mins": 18
  },
  {
    "Location": "Falconridge Club - Service Location",
    "Club": "Boys and Girls Clubs of Calgary",
    "Total time offline in mins": 17
  },
  {
    "Location": "Carleton Village Jr and Sr PS - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 17
  },
  {
    "Location": "Grandravine Youth Centre TCHC - Service Location",
    "Club": "St. Alban's Boys and Girls Club",
    "Total time offline in mins": 17
  },
  {
    "Location": "Boys and Girls Club of London - Service Location",
    "Club": "Boys and Girls Club of London",
    "Total time offline in mins": 16
  },
  {
    "Location": "Eastview Arena-Skate the Dream - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 16
  },
  {
    "Location": "Saint- Jean - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 16
  },
  {
    "Location": "BGCOA Main Building - Service Location",
    "Club": "Boys & Girls Club of Olds & Area",
    "Total time offline in mins": 15
  },
  {
    "Location": "Bowmanville High School - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 15
  },
  {
    "Location": "Chelsea Gardens  - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 15
  },
  {
    "Location": "Dunrankin Public School - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 15
  },
  {
    "Location": "Let's Get Moving- Roxborough Park Junior Public School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 15
  },
  {
    "Location": "Let's Get Moving- Woodward School - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 15
  },
  {
    "Location": "St. John Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 15
  },
  {
    "Location": "Oshawa Civic Centre - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 14
  },
  {
    "Location": "Rolling Hills Club at Rolling Hills Public School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 13
  },
  {
    "Location": "Core Neighbourhood Club – RRTG Program Location - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 11
  },
  {
    "Location": "Central Tech TDSB - Service Location",
    "Club": "Toronto Kiwanis Boys and Girls Clubs",
    "Total time offline in mins": 11
  },
  {
    "Location": "Langton Club at Langton Public School - Service Location",
    "Club": "Boys and Girls Clubs of Kawartha Lakes",
    "Total time offline in mins": 10
  },
  {
    "Location": "Groupe Action jeunesse Charlevoix - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 10
  },
  {
    "Location": "Main Club House/Before/ASP/Summer/Evening  Prog - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 8
  },
  {
    "Location": "Lake Simcoe Public School - Service Location",
    "Club": "Boys and Girls Club of York Region",
    "Total time offline in mins": 8
  },
  {
    "Location": "Petite-Rivière-St-François - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 8
  },
  {
    "Location": "Ecole Olds Elementary School - Service Location",
    "Club": "Boys & Girls Club of Olds & Area",
    "Total time offline in mins": 7
  },
  {
    "Location": "Howard Coad Mini Club - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 7
  },
  {
    "Location": "Saskatoon Prairieland Exhibition - Service Location",
    "Club": "Boys and Girls Clubs of Saskatoon",
    "Total time offline in mins": 7
  },
  {
    "Location": "Milltown After School Program - Service Location",
    "Club": "Boys & Girls Club of Charlotte County",
    "Total time offline in mins": 6
  },
  {
    "Location": "Banbury Child Care Centre/Preschool/Before and ASP - Service Location",
    "Club": "Boys and Girls Club of Brantford",
    "Total time offline in mins": 6
  },
  {
    "Location": "L'Illusion - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 6
  },
  {
    "Location": "Boys & Girls Club of Olds & Area - Main Club",
    "Club": "Boys & Girls Club of Olds & Area",
    "Total time offline in mins": 4
  },
  {
    "Location": "West Riverview Elementary - Service Location",
    "Club": "Boys and Girls Club of Riverview",
    "Total time offline in mins": 4
  },
  {
    "Location": "Ontario Early Years Centre- Hillcrest Site - Service Location",
    "Club": "Boys and Girls Clubs of Hamilton",
    "Total time offline in mins": 4
  },
  {
    "Location": "Ontario Shores - Service Location",
    "Club": "Boys and Girls Club of Durham",
    "Total time offline in mins": 3
  },
  {
    "Location": "Galloway Ontario Early Years Centre & Main Club Site - Service Location",
    "Club": "Boys and Girls Club of East Scarborough",
    "Total time offline in mins": 3
  },
  {
    "Location": "McHardy/Fair Oaks Place - Service Location",
    "Club": "Boys and Girls Club of Peel",
    "Total time offline in mins": 3
  },
  {
    "Location": "The Club - Service Location",
    "Club": "Boys and Girls Club of Airdrie",
    "Total time offline in mins": 2
  },
  {
    "Location": "North Burnaby Club - Service Location",
    "Club": "Boys and Girls Clubs of South Coast BC",
    "Total time offline in mins": 2
  },
  {
    "Location": "Pope Paul VI Catholic School - Service Location",
    "Club": "Dovercourt Boys and Girls Club",
    "Total time offline in mins": 2
  },
  {
    "Location": "L'Intrépide - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 2
  },
  {
    "Location": "MDJ Clermont - Service Location",
    "Club": "Régional des maisons de jeunes de Québec",
    "Total time offline in mins": 2
  },
  {
    "Location": "First Steps Centre - Service Location",
    "Club": "Boys and Girls Club of Kamloops",
    "Total time offline in mins": 1
  },
  {
    "Location": "Boys and Girls Club of Preston - Main Club",
    "Club": "Boys and Girls Club of Preston",
    "Total time offline in mins": 1
  },
  {
    "Location": "Greenholme Junior Middle School - Service Location",
    "Club": "Braeburn Boys and Girls Club",
    "Total time offline in mins": 1
  },
  {
    "Location": "Petitcodiac Boys and Girls Club Inc - Service Location",
    "Club": "Petitcodiac Boys and Girls Club Inc.",
    "Total time offline in mins": 1
  }
]

users = {
    "John Doe": {
        "locations": [
            "Central Tech TDSB - Service Location"
        ],
        "log": {
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

          bigTime = datetime.now(pytz.utc).strftime(bigFormat)

          if (location not in locations):
               locations[location] = {
                    "latitude": 0,
                    "longitude": 0,
                    "log": {}
               }

          addTimeToLog(locations[location]["log"], bigTime, loggedTime)

          if (not name in users):
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
     now = datetime.now(pytz.utc)
     offlineTime = 0
     times = 0

     if (now.strftime(bigFormat) in log):
          offlineTime += log[now.strftime(bigFormat)]["total"]
          times += log[now.strftime(bigFormat)]["times"]

     for x in range(1, maxTimeUnits):
          tmpTime = now - timedelta(minutes=x)
          if (tmpTime.strftime(bigFormat) in log):
               offlineTime += log[tmpTime.strftime(bigFormat)]["total"]
               times += log[tmpTime.strftime(bigFormat)]["times"]

     mood = round(100 * min(100, offlineTime/maxTimeRecord), 0)

     temperment = round(100 - min(100, 100 * times/maxOnOffTimes), 0)

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

### LOCATIONS ###
class Locations(Resource):
     def get(self):
          parser = reqparse.RequestParser()
          parser.add_argument("location")
          args = parser.parse_args()
          location = args["location"]
          location = location.replace("_", " ")

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

### DATA ###
@app.route("/data")
def getData():
     parser = reqparse.RequestParser()
     parser.add_argument("return")
     args = parser.parse_args()

     if args["return"] == "json":
          data = []
          for location in locations:
               loc = locations[location]
               club = loc["club"]
               total = 0
               for item in loc["log"]:
                    total = total + loc["log"][item]["total"]
               totalInMinute = floor(total / (1000 * 60))
               data.append(
                    {
                         "location": location,
                         "club": club,
                         "timeOffline": totalInMinute
                    }
               )
          for fake in fakeResponse:
               data.append(
                    {
                         "location": fake["Location"],
                         "club": fake["Club"],
                         "timeOffline": fake["Total time offline in mins"]
                    }
               )
          return json.dumps(data), 200
     else:
          data = "Location,Club,Total time offline in mins\n"
          for location in locations:
               loc = locations[location]
               club = loc["club"]
               total = 0
               for item in loc["log"]:
                    total = total + loc["log"][item]["total"]
               totalInMinute = floor(total / (1000 * 60))
               data = data + "{0},{1},{2}\n".format(location, club, totalInMinute)
          for fake in fakeResponse:
               data = data + "{0},{1},{2}\n".format(fake["Location"],fake["Club"],fake["Total time offline in mins"])
          return Response(
               data,
               mimetype="text/csv",
               headers={"Content-disposition": "attachment; filename=data.csv"}
          )

@app.route("/data/clear", methods=['POST'])
def clearData():
      for user in users:
        users[user]["log"] = {}
      locations["Central Tech TDSB - Service Location"]["log"] = {}
      return "Data cleared!", 200

### FLASK SETUP ###
api.add_resource(Pets, "/pets")
api.add_resource(Users, "/users")
api.add_resource(Locations, "/locations")

if __name__ == '__main__':
     app.debug = True
     app.run(host='0.0.0.0')