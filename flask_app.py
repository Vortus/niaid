import os
from flask import Flask
from flask_restful import Api
from src.niaid.niaid import setup_api

app = Flask(__name__)
api = Api(app)
setup_api(api)

if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)