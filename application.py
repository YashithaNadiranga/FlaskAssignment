from flask import Flask,render_template,request, make_response
from flask import jsonify
from flask_pymongo import PyMongo
from flask_pymongo import ObjectId

application = Flask(__name__)
application.config["MONGO_URI"] = "mongodb+srv://feanixlabs:feanixlabs@cluster0.ksxrr.mongodb.net/loan?retryWrites=true&w=majority"
mongodb_client = PyMongo(application)
db = mongodb_client.db

@application.route('/', methods=["GET","POST"])
def route_home():
    return render_template('index.html')

@application.route('/deposit', methods=["GET","POST"])
def route_deposit():
    if request.method =='POST':
        name = request.form['name']
        amount = request.form['amount']
        db.users.insert_one({"name": name, "amount": int(amount)})
    return render_template('deposit.html')

@application.route('/getloan', methods=["GET","POST"])
def route_getloan():
    response = []
    if request.method =='GET':
        data = db.users.find()
        for document in data:
            document['_id'] = str(document['_id'])
            response.append(document)
    if request.method =='POST':
        name = request.form['name']
        guarantee = request.form['guarantee']
        amount = request.form['amount']
        if(name != guarantee):
            user = db.users.find_one({"_id":ObjectId(name)})
            guaranteeDetails = db.users.find_one({"_id":ObjectId(guarantee)})
            aligibalAmount = user['amount'] + guaranteeDetails['amount']
            if(aligibalAmount >= int(amount)):
                db.loans.insert_one({"user": ObjectId(name), "guarantee": ObjectId(guarantee), "amount": int(amount), "state": "active"})

        # db.users.insert_one({"name": name, "amount": int(amount)})
    return render_template('getLoan.html', users=response)

@application.route('/payloan', methods=["GET","POST"])
def route_payloan():
    return render_template('payloan.html')


if __name__ == '__main__':
    application.run(debug=True)