from app import app          
from app.database import Database   
from app import email    

from flask import render_template, request, url_for, redirect, session
import datetime
import itertools
from bson.objectid import ObjectId

# Function returning main data for the veld page
def coreF(queryDate):
    # Find reports with query date and issue
    veld_reports = Database.find("reports",queryDate,"veld")
    # Find all dates with reports
    FindDates = Database.findDates("reports","veld")

    return [veld_reports,FindDates]

@app.route('/login/veld_dash/',methods=['POST','GET'])
def veld_dash():
    # Set today's date
    TODAY = datetime.datetime.today().date()
    username= session['username']
    
    queryDate = session['todayDate']

    # Check if its a POST request, and change queryDate
    if request.method == 'POST':
        queryDate = datetime.datetime.strptime(request.form['qDate'], '%Y-%m-%d')
    # Get veld reports and found dates
    veld_reports = coreF(queryDate)[0] 
    FindDates = coreF(queryDate)[1]
    
    return render_template('veld_dash.html',veld_reports=veld_reports,TODAY=queryDate, FindDates=FindDates)

@app.route('/login/veld_dah/',methods=['POST','GET'])
def attend():
    # Update Attended, make it true
    veld_id = request.form['_id']
    query = {"_id": ObjectId(veld_id)}
    new_value = {"$set":{"Attended":True}}
    Database.update_one("reports",query,new_value)
    msg = 'Issue Addressed'
    #Get and set queryDate 
    queryDate = datetime.datetime.strptime(request.form['qDate1'], '%Y-%m-%d')
    # Get veld reports and found dates
    veld_reports = coreF(queryDate)[0] 
    FindDates = coreF(queryDate)[1]

    # Send email with provided details
    content = f"""
            Dear Sir/Ma'am \n

            We would like to take this opportunity to thank you for reporting the veld fire on {queryDate.strftime('%Y-%m-%d')}\n
            This Email is to inform you that the issue has been addressed.\n

            Yours Thankful
            EMA Team
      """
    email.sendEmail('EMA Response',content,request.form['rEmail'])

    return render_template('veld_dash.html',veld_reports=veld_reports,TODAY=queryDate, FindDates=FindDates)
