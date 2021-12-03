from app import app          
from app.database import Database     
from app import email 

from flask import render_template, request, url_for, redirect, session
import datetime
import itertools
from bson.objectid import ObjectId

# Function returning main data for the litter page
def coreF(queryDate):
    # Find reports with query date and issue
    litter_reports = Database.find("reports",queryDate,"littering")
    # Find all dates with reports
    FindDates = Database.findDates("reports","littering")

    return [litter_reports,FindDates]

@app.route('/login/litter_dash/',methods=['POST','GET'])
def litter_dash():
    # Set today's date
    TODAY = datetime.datetime.today().date()
    username= session['username']
    
    queryDate = session['todayDate']
    # Check if its a POST request, and change queryDate
    if request.method == 'POST':
        queryDate = datetime.datetime.strptime(request.form['qDatel2'], '%Y-%m-%d')
    
    # Get veld reports and found dates
    litter_reports = coreF(queryDate)[0] 
    FindDates = coreF(queryDate)[1]
    
    return render_template('litter_dash.html',litter_reports=litter_reports,TODAY=queryDate, FindDates=FindDates)

@app.route('/login/litter_dah/',methods=['POST','GET'])
def attend_litter():
    # Update Attended, make it true
    litter_id = request.form['_id']
    #doat = datetime.datetime.strptime(request.form['dtest'], '%Y-%m-%d')
    query = {"_id": ObjectId(litter_id)}
    new_value = {"$set":{"Attended":True}}
    Database.update_one("reports",query,new_value)
    msg = 'Issue Addressed'
    #Get and set queryDate 
    queryDate = datetime.datetime.strptime(request.form['qDatel'], '%Y-%m-%d')
    # Get veld reports and found dates
    litter_reports = coreF(queryDate)[0] 
    FindDates = coreF(queryDate)[1]
    # Send email with provided details
    content = f"""
            Dear Sir/Ma'am \n

            We would like to take this opportunity to thank you for reporting the Littering on {queryDate.strftime('%Y-%m-%d')}\n
            This Email is to inform you that the issue has been addressed.\n

            Yours Thankful
            EMA Team
      """
    email.sendEmail('EMA Response',content,request.form['rEmail'])

    return render_template('litter_dash.html',litter_reports=litter_reports,TODAY=queryDate, FindDates=FindDates)
