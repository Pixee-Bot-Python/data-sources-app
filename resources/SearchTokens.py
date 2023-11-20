from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from flask import request, jsonify
import datetime
import uuid
import os
import requests

BASE_URL = os.getenv("VUE_APP_BASE_URL")

class SearchTokens(Resource):
    def __init__(self, **kwargs):
        self.psycopg2_connection = kwargs["psycopg2_connection"]


    def get(self, endpoint, arg1, arg2=''):        
        try:
            data_sources = {"count": 0, "data": []}
            if type(self.psycopg2_connection) == dict:
                return data_sources        

            cursor = self.psycopg2_connection.cursor()
            token = uuid.uuid4().hex
            expiration = datetime.datetime.now() + datetime.timedelta(minutes=5)
            cursor.execute(f"insert into access_tokens (token, expiration_date) values (%s, %s)", (token, expiration))         
            self.psycopg2_connection.commit()

            headers = {"Authorization": f"Bearer {token}"}
            if endpoint == "quick-search":
                r = requests.get(f"{BASE_URL}/quick-search/{arg1}/{arg2}", headers=headers)
                return r.json()
            
            elif endpoint == "data-sources":
                r = requests.get(f"{BASE_URL}/data-sources/{arg1}", headers=headers)
                return r.json()
            
            else:
                return {"error": "Unknown endpoint"}

        except Exception as e:
            self.psycopg2_connection.rollback()
            print(str(e))
            return {"error": e}
        
