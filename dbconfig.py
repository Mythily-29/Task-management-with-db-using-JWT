from pymongo import MongoClient,ASCENDING,DESCENDING
from datetime import datetime


client=MongoClient('mongodb://localhost:27017/')

db=client['task_management']

signed_table=db['signup']

task_table=db['tasks']

class Database:
    
    def insert_user(self,data):
        signed_table.insert_one(data)
    def find_one(self,data):
        return signed_table.find_one({'email':data})
    def update(self,data,email):
        signed_table.update_many({'email':email},{"$set":data}) 
    def get_users(self,id=None):
        if not id:
            return signed_table.find({},{"password":0,"_id":0})
        else:
            return signed_table.find({"user_id":id},{"password":0,"_id":0})

class Task_operations:

    def insert_task(self,data):
        task_table.insert_one(data)

    def update_task(self,id,data):
        task_table.update_many({'task_id':id},{"$set":data})

    def find_task_id(self,id,email):
        return task_table.find_one({'task_id':id,'email':email},{"_id":0})
    
    def delete_tasks(self,id):
         task_table.delete_one({"task_id":id})

    def filter_status(self,email,status):
        return task_table.find({"email":email,"status":status},{'_id':0})
    
    def filter_priority(self,email, priority):
        return task_table.find({"email":email,"priority":priority},{'_id':0})
    
    def sort_duedate(self,email, order = 'asc'):
        sorting = ASCENDING if order == 'asc' else DESCENDING
        return task_table.find({"email":email},{"_id":0}).sort("due_date",sorting)
    
    def get_tasks(self,email=None,id=None):
        if email:
            return task_table.find({"email":email},{"_id":0})
        else:
            return task_table.find({"task_id":id},{"_id":0})


def check_date_format(input_format):
    try:
        res=datetime.strptime(input_format, "%Y-%m-%d")
        return True
    except Exception:
        return False
    


