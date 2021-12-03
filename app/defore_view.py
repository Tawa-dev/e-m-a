from app import app          
from app.database import Database      
from app import email    

from flask import render_template, request, url_for, redirect, session
import datetime
import itertools
from bson.objectid import ObjectId


# Function returning main data for the deforestation page
def coreF(queryDate):
    # Find reports with query date and issue
    defore_reports = Database.find("reports",queryDate,"deforestation")
    # Find all dates with reports
    FindDates = Database.findDates("reports","deforestation")

    return [defore_reports,FindDates]

@app.route('/login/defore_dash/',methods=['POST','GET'])
def defore_dash():
    # Set today's date
    TODAY = datetime.datetime.today().date()
    username= session['username']
    
    queryDate = session['todayDate']
    # Check if its a POST request, and change queryDate
    if request.method == 'POST':
        queryDate = datetime.datetime.strptime(request.form['qDated2'], '%Y-%m-%d')
    
    # Get veld reports and found dates
    defore_reports = coreF(queryDate)[0] 
    FindDates = coreF(queryDate)[1]
    
    return render_template('defore_dash.html',defore_reports=defore_reports,TODAY=queryDate, FindDates=FindDates)

@app.route('/login/defore_dah/',methods=['POST','GET'])
def attend_defore():
    # Update Attended, make it true
    defore_id = request.form['_id']
    query = {"_id": ObjectId(defore_id)}
    new_value = {"$set":{"Attended":True}}
    Database.update_one("reports",query,new_value)
    msg = 'Issue Addressed'
    #Get and set queryDate 
    queryDate = datetime.datetime.strptime(request.form['qDated'], '%Y-%m-%d')
    # Get veld reports and found dates
    defore_reports = coreF(queryDate)[0] 
    FindDates = coreF(queryDate)[1]
    # Send email with provided details
    content = f"""
            Dear Sir/Ma'am \n

            We would like to take this opportunity to thank you for reporting the deforestation on {queryDate.strftime('%Y-%m-%d')}\n
            This Email is to inform you that the issue has been addressed.\n

            Yours Thankful
            EMA Team
      """
    email.sendEmail('EMA Response',content,request.form['rEmail'])

    return render_template('defore_dash.html',defore_reports=defore_reports,TODAY=queryDate, FindDates=FindDates)
