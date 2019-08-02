
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
import pymongo
import random
from datetime import datetime  
from datetime import timedelta
import doctest
from itertools import permutations 
import dns
from flask import render_template,flash,redirect
from flask import request
from flask import Flask, render_template, url_for, flash, redirect
#from matplotlib import pyplot as plt

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import array as arr
app = Flask(__name__)

R = 0
I = 0
A = 0
POWER_PLANT=1000
array1 = arr.array('i', [])
array2 = arr.array('i', [])

myclient = pymongo.MongoClient("mongodb+srv://ankita:ankita87@cluster0-rlpsr.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["MY_FIRST_DATABASE"]
        

  

@app.route("/home")
def home():

    return render_template('home.html')
@app.route("/dashboard")
def demo():
    
    return render_template('dash.html',
    Residential_Demand=request.args.get('Residential_Demand'),
    Industrial_Demand=request.args.get('Industrial_Demand'),
    Agricultural_Demand=request.args.get('Agricultural_Demand'),
    Residential_Manage=request.args.get('Residential_Manage'),
    Industrial_Manage=request.args.get('Industrial_Manage'), 
    Agricultural_Manage=request.args.get('Agricultural_Manage'),
    time=request.args.get('time'),
    h =request.args.get('h'))


@app.route("/credits")
def credits():

    return render_template('credits.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
        if request.form['userid'] != 'admin' or request.form['psw'] != 'admin':
             error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
  return render_template('login.html', error=error) 
  
@app.route("/dashboard", methods=['GET', 'POST'])


def dashboard():
    
  
  if request.method == 'POST':
    d=request.form['date']
    m=request.form['month']
    y=request.form['year']
    h=request.form['hour']
    hour1=str(h)
   
        
           
    timestampStr1 = str(d)+'-' +str(m)+'-' +str(y)
        
    mycol = mydb[timestampStr1]
    myquery={"TIME":hour1}
    for x in mycol.find(myquery):
        
        R = x["Residential"]
        I = x["Industrial"]
        A = x["Agricultural"]
       
        array1.insert(0,int(R) )
        array1.insert(1,int(I))
        array1.insert(2,int(A) )   
        
        
    Actual_Demand = (array1[0]+array1[1]+array1[2])

    PLANT_CAPACITY=int((Actual_Demand*(70/100)))
   
    if (R > I) and (R > A):
     array1.insert(3,int(R))
     r = PLANT_CAPACITY - int(R)
     R1=int(R)
     A1 = 0
     I1 = r

    elif (I > R) and (I > A):
       array1.insert(3,int(I))
       r = PLANT_CAPACITY - int(I)
       I1 = int(I)
       R1 = r/2
       A1 = r/2
    
    else:

       array1.insert(3,int(A))
       r = PLANT_CAPACITY - int(A)
       A1=int(A)
       I1 = r
       R1 = 0
     
    Res = int(R)
    ind = int(I)
    Agri = int(A)
    Res1 = int(R1)
    ind1 = int(I1)
    Agri1 = int(A1)
        
    if (d == '3') or (y == '2018'):
        return redirect(url_for('home'))
    else:
        return render_template('dash.html',
        Residential_Demand = Res,
        Industrial_Demand = ind,
        Agricultural_Demand=Agri,
        Residential_Manage=Res1, Industrial_Manage=ind1, Agricultural_Manage=Agri1,time=timestampStr1,h=hour1)
            
 





@app.route('/developers')
def developers():
  return render_template('developers.html')
  



app.run()
