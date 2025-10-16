from flask import Flask,request,jsonify
from authentication import Authentication,Task,Task_operations
from validations import check_token_expiry,get_jwt_email
from dbconfig import Database

app=Flask(__name__)

authentication=Authentication()
task=Task()
task_op=Task_operations()
database=Database()

@app.route('/signup',methods=['POST'])
def signup_user():
    data = request.get_json()
    return authentication.signup(data)

@app.route('/login',methods=['POST'])
def login_user():
    data=request.get_json()
    return authentication.login(data)

#for other protected apis

@app.route('/getusers',methods=['GET'])
def get_users():
    result=list(database.get_users())
    if result:
         return jsonify({'data':result}),200
    else:
        return jsonify({'data':'No data found'})
    
@app.route('/getusers/<int:id>',methods=['GET'])
@check_token_expiry
def get_single_user(id):
    result=list(database.get_users(id))
    if result:
         return jsonify({'data':result}),200
    else:
        return jsonify({'data':'No data found'})

@app.route('/updateuser',methods=['POST'])
@check_token_expiry
def update_user():
   data=request.get_json()
   return authentication.signup(data,name='update')

@app.route('/createtask',methods=['POST'])
@check_token_expiry
def create_task():
    data=request.get_json()
    return task.create_task(data)

@app.route('/updatetask/<int:id>',methods=['POST'])
@check_token_expiry
def update_task(id):
    data=request.get_json()
    return task.create_task(data,id,name='update')

@app.route('/deletetask/<int:id>',methods=['DELETE'])
@check_token_expiry
def delete_task(id):
    return task.delete_task(id)

@app.route('/tasks_status/status/<status>', methods = ['GET'])
@check_token_expiry
def filtering(status):
    currentemail=get_jwt_email()
    result = list(task_op.filter_status(currentemail,status))
    if result:
         return jsonify({'data':result}),200
    else:
        return jsonify({'data':'No data found'})

@app.route('/tasks_priority/<priority>', methods = ['GET'])
@check_token_expiry
def priority_filter(priority):
    currentemail=get_jwt_email()
    result = list(task_op.filter_priority(email=currentemail,priority=priority))
    if result:
         return jsonify({'data':result}),200
    else:
        return jsonify({'data':'No data found'})
    
@app.route('/tasks_duedate_asc/', methods = ['GET'])
@check_token_expiry
def duedate_asc():
    currentemail=get_jwt_email()
    result = list(task_op.sort_duedate(currentemail,order = 'asc'))
    return jsonify({'data':result}), 200

@app.route('/tasks_duedate_dsc/', methods = ['GET'])
@check_token_expiry
def duedate_desc():
    currentemail=get_jwt_email()
    result = list(task_op.sort_duedate(currentemail,order = 'desc'))
    return jsonify({'data':result}), 200

@app.route('/gettask/<email>',methods=['GET'])
@check_token_expiry
def get_task(email):
    if email==get_jwt_email():
        result=list(task_op.get_tasks(email))
        if result:
            return jsonify({'data':result}),200
        else:
            return jsonify({'message':'No data found'}),200
    else:
        return jsonify({'message':'You are not authenticated to see other tasks'}),401
    
@app.route('/gettask/<int:id>',methods=['GET'])
@check_token_expiry
def get_single_task(id):
    now_email=get_jwt_email()
    data=task_op.find_task_id(id,now_email)
    if data:
        return jsonify({'data':data}),200
    else:
        return jsonify({'message':'No data found'}),200

@app.route('/gettask/<status>/<date>/<priority>')
@check_token_expiry
def filtered(status,date,priority):
    currentemail=get_jwt_email()
    result = list(task_op.filter_priority(email=currentemail,status=status,date=date,priority=priority))
    if result:
         return jsonify({'data':result}),200
    else:
        return jsonify({'data':'No data found'})


if __name__=="__main__":
    app.run(debug=True)


