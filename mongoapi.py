# -*- coding: utf-8 -*-
"""
@author: vijayana
"""
from flask import Flask,request
from flask import jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'testing'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/testing'

mongo = PyMongo(app)

@app.route('/eventlist')
def get_all():
  user = mongo.db.events
  #user.insert({'name': 'testing'})
  #username = request.args.get('name')
  output = []
  for s in user.find():
    #if username == s['name']:  
      output.append({'name' : s['name']})
  return jsonify(output)

@app.route('/addevent')
def addevent():
  user = mongo.db.events
  eventname = request.args.get('ename')
  eventdescription = request.args.get('edesc')
  if eventname and eventdescription:
      user.insert({'eventname': eventname ,'eventdescription': eventdescription})
      return eventname+" "+eventdescription +" Added"
  else:
      return "Dude, u r missing fields!"
  
  return "Done adding"

@app.route('/addquestion')
def addquestion():
  user = mongo.db.questiongrps
  eventname = request.args.get('ename')
  question = request.args.get('question')
  if eventname and question:
      user.insert({'eventname': eventname ,'question': question,'yrescount':0,'nrescount':0})
      return eventname+" "+ question +" Added"
  else:
      return "Dude, u r missing fields!"
  
  return "Done adding"

@app.route('/search')

def search():
 # eventstr = request.args.get('searchstr')
  output=[]
 # if eventstr:
  user = mongo.db.events
  for s in user.find():
     output.append({'eventname' : s['eventname']})
  return jsonify(output)

@app.route('/questions')

def questions():
  eventstr = request.args.get('searchstr')
  output=[]
  if eventstr:
    user = mongo.db.questiongrps
    for s in user.find({'eventname' : eventstr}):
     output.append({'question' : s['question'],'yrescount' : s['yrescount'],'nrescount' : s['nrescount']})
  return jsonify(output)

@app.route('/answer')

def answer():
  eventstr = request.args.get('event')
  ques = request.args.get('question')
  ans = request.args.get('answer')
  ycount=0;
  ncount=0;
  if eventstr and ques and ans :
    user = mongo.db.questiongrps
    for s in user.find({'eventname' : eventstr, 'question':ques}):
       ycount = s['yrescount']
       ncount = s['nrescount']
    if ans=="yes":   
      user.update({'eventname' : eventstr, 'question':ques},{'$set': {'yrescount': ycount + 1}}, upsert=False, multi=False)
    if ans=="no":   
      user.update({'eventname' : eventstr, 'question':ques},{'$set': {'nrescount': ncount + 1}}, upsert=False, multi=False)  
    
  return "Done!!"


@app.route('/event/<eventname>')

def eventpage(eventname):
 # eventstr = request.args.get('searchstr')
  output=[]
 # if eventstr:
  user = mongo.db.events
  for s in user.find():
     output.append({'eventname' : s['eventname']})
  return jsonify(output)

@app.route('/testing')

def testing():

     return "<h1>Just,...Tesing dude!</h1>"

if __name__ == "__main__":

    app.run()