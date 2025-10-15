from flask import jsonify,request
from validations import email_exists,get_jwt_email
from dbconfig import Database,Task_operations,check_date_format
import jwt
import datetime
import random

secret_key='1234'

database=Database()
task_op=Task_operations()

id_generate=[1,2,3,4,5,6,7,8,9,0]

class Authentication:

    def signup(self,data,name=None):

        required_fields=["username","email","password"]

        for i in required_fields:
            if i not in data or not str(data[i]).strip():
                return jsonify({'message':f'{i} field is missing',"status":400})

        if len(str(data['password'])) < 5:
            return jsonify({'message':f'Password length is short',"status":400})
        elif '@' not in data['email']:
            return jsonify({'message':'Invalid email format',"status":400})
        
        if name:
            get_email=get_jwt_email()
            if get_email:
                database.update(data,get_email)
                expiry=datetime.datetime.utcnow()+datetime.timedelta(minutes=1)
                payloads={'email':data['email'],'expiry_time':expiry.timestamp()}
                sign=jwt.encode(payloads,secret_key,algorithm='HS256')
                return jsonify({'message':'Updated successfully','email':data['email'],'token':sign})
            
        if email_exists(data['email']):
            return jsonify({"message":'Email already exists try some other',"status":400})
        
        random_id=int(''.join(map(str,random.sample(id_generate,k=3))))
        data['user_id']=random_id

        if not name:
            database.insert_user(data)
        return jsonify({"message":"success","status":200})
    
    def login(self,data):

        required_fields=['email','password']

        for i in required_fields:
            if i not in data or not str(data[i]).strip():
                return jsonify({'message':f'{i} field is missing',"status":400})
            
        result=database.find_one(data['email'])

        if result:
            if data['password']==result['password']:
                expiry=datetime.datetime.utcnow()+datetime.timedelta(minutes=1)
                payload={'email':result['email'],'expiry_time':expiry.timestamp()}
                sign=jwt.encode(payload,secret_key,algorithm='HS256')
                return jsonify({'email':result['email'],'token':sign})
                
            else:
                return jsonify({'message':'Your password is wrong',"status":400})
        else:
            return jsonify({"message":"Your details are invalid","status":400})


class Task:

    def create_task(self,data,id=None,name=None):

        required_fields=["email","taskname","priority","status","due_date"]
        priority_names=['high','low','medium']
        status_names=['pending','progress','completed']

        for i in required_fields:
            if i not in data or not str(data[i]).strip():
                return jsonify({'message': f'{i} field is missing or empty', "status": 400})

        if data['priority'].lower() not in priority_names or data['status'].lower() not in status_names:
                return jsonify({
                    'message': "Priority must be one of ['high', 'low', 'medium'] and status must be one of ['pending', 'progress', 'completed']",
                    'status': 401
                })
        
        valid_date=check_date_format(data['due_date'])
        if not valid_date:return jsonify({'message':'Wrong date format'})
        
        get_email=get_jwt_email()

        if name and id:
            if data['email'] != get_email:
                return jsonify({'message':'Email should not to be changed same login email should be use'}),401
            else:
                get_id=task_op.find_task_id(id,data['email'])
                if get_id:
                    task_op.update_task(id,data)
                    return jsonify({'message':'Data updated successfully'}),200
                else:
                    return jsonify({'message':'Cannot fetch the id that you entered'})

        if data['email']==get_email:
            task_id=int(''.join(map(str,random.sample(id_generate,k=3))))
            data['task_id']=task_id
            task_op.insert_task(data)
            return jsonify({'Task id':task_id,'message':'Task created successfully'}),200
        else:
            return jsonify({'message':'Cannot fetch the email'}),401

    def delete_task(self,id):
        get_email=get_jwt_email()
        get_id=task_op.find_task_id(id,get_email)

        if get_id:
            task_op.delete_tasks(id)
            return jsonify({"message":'Task deleted successfully',"Task_id":get_id}),200
        else:
            return jsonify({"message":"Cannot find the task ID"}),401
    
