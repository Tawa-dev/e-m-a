from app import app          
from app.database import Database   
import datetime   

from flask import render_template, request, url_for, redirect, session

@app.route('/')
def home():
    return render_template('home.html')

#Veld Fire View
@app.route('/veld', methods = ['POST','GET'])
def veld():
     # Initialize msg, date and time to current date and time
    msg=''
    DOR = datetime.datetime.today().date()
    TOR = datetime.datetime.today().time()
    if request.method == 'POST':
        issue = request.form['issue']
        dor = datetime.datetime.strptime(request.form['dor'], '%Y-%m-%d') #date of report
        tor = request.form['tor']                  #time of report
        location = request.form['address']

        # Insert fire report details
        veld = {"Date_Of_Report":dor,"Time_Of_Report":tor, "Location": location,"Issue":issue,"Attended":False}
        Database.insert("reports",veld)
        msg = 'Veld Fire Reported! Thank You!'

    return render_template('veld.html',DOR = DOR,TOR = TOR,address = "location",msg=msg)

# Deforestation View
@app.route('/deforestation',methods =['POST','GET'])
def deforestation():
    # Initialize msg, date and time to current date and time
    msg=''
    DOR = datetime.datetime.today().date()
    TOR = datetime.datetime.today().time() 
    if request.method == 'POST':
        issue = request.form['issue']
        dor = datetime.datetime.strptime(request.form['dor'], '%Y-%m-%d') #date of report
        tor = request.form['tor']                  #time of report
        location = request.form['address']

        # Insert fire report details
        defore = {"Date_Of_Report":dor,"Time_Of_Report":tor, "Location": location,"Issue":issue,"Attended":False}
        Database.insert("reports",defore)
        msg = 'Deforestation Reported! Thank You!'

    return render_template('deforestation.html',DOR = DOR,TOR = TOR,address = "location",msg=msg)
    

# Littering View
@app.route('/littering',methods =['POST','GET'])
def litter():
     # Initialize msg, date and time to current date and time
    msg=''
    DOR = datetime.datetime.today().date()
    TOR = datetime.datetime.today().time() 
    if request.method == 'POST':
        issue = request.form['issue']
        dor = datetime.datetime.strptime(request.form['dor'], '%Y-%m-%d') #date of report
        tor = request.form['tor']                  #time of report
        location = request.form['address']

        # Insert fire report details
        litter = {"Date_Of_Report":dor,"Time_Of_Report":tor, "Location": location,"Issue":issue,"Attended":False}
        Database.insert("reports",litter)
        msg = 'Littering Reported! Thank You!'

    return render_template('litter.html',DOR = DOR,TOR = TOR,address = "location",msg=msg)
    