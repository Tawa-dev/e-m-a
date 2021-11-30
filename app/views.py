from app import app          
from app.database import Database      

from flask import render_template, request, url_for, redirect, session
import re
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


app.secret_key = "testing"




# this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Set today's date
    #TODAY = datetime.datetime.today().date()
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Fetch one record and return result
        user = Database.find_one("users",{'username':username,"password":password})
        # Check if user does have a user
        if user:
           user = user
           # Create session data, we can access this data in other routes
           session['loggedin'] = True
           session['username'] = user['username']
           doat = datetime.datetime.strptime(request.form['dtest'], '%Y-%m-%d')
           session['todayDate'] = doat
           # Redirect to dashboard page
           return redirect(url_for('dashboard'))
        else:
            # Password is wrong
            msg = 'Username / Password is wrong!'
       
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg,doa = datetime.datetime.today().date())

# this will be the logout page
@app.route('/login/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   #session.pop('_id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

#  this will be the dashboard, only accessible for loggedin users
@app.route('/login/dashboard')
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the admit page 
        username = session['username']

        return redirect(url_for('veld_dash'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    

   