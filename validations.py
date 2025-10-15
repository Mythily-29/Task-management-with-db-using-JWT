from dbconfig import Database
from functools import wraps
from flask import Flask,request,jsonify
import jwt
import datetime

secret_key='1234'

database=Database()

def email_exists(email):

    data=database.find_one(email)
    return True if data else False

def check_token_expiry(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        auth=request.headers.get('Authorization')
        if not auth:
            return jsonify({'message':'Field is not provided'})
        
        if auth:
            try:
                token=auth.split(' ')[1]
                payload=jwt.decode(token,secret_key,algorithms=['HS256'])
                expiry_timestamp=payload.get('expiry_time')

                expiry_time = datetime.datetime.fromtimestamp(expiry_timestamp)
                current_time = datetime.datetime.utcnow()

                if current_time > expiry_time:
                    return jsonify({'message':'Token Expired Login again'}),401
            except jwt.DecodeError:
                return jsonify({'message':'Token is not provided'}),401

        return f(*args,**kwargs)
    return wrapper


def get_jwt_email():
    auth=request.headers.get('Authorization')
    if not auth:
        return jsonify({'message':'Field is not provided'})
    
    if auth:
        try:
            token=auth.split(' ')[1]
            payload=jwt.decode(token,secret_key,algorithms=['HS256'])
            print(payload)
            return payload.get('email')
        except Exception as e:
            return ({'message':e}),401
        




    



