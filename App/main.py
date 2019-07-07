from flask import Flask, render_template, Markup, request, redirect, session, abort, url_for, flash
#from flask_session import Session
from functools import wraps
 
import requests
import json
from flask import jsonify

import time
import random
import moment

import pytz
from datetime import datetime, timezone, date, time, timedelta

import os
import tempfile
from werkzeug.utils import secure_filename

# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import storage

# Simulation
from faker import Faker

# Google Translate
from googletrans import Translator

#Notifications
import onesignal as onesignal_sdk

# Mailing
from flask_mail import Mail
from flask_mail import Message

#Import for Firebase Notifications
# Send to single device.
from pyfcm import FCMNotification

import class_form

from dotenv import load_dotenv
load_dotenv(verbose=True)

SECRET_KEY = os.getenv("SECRET_KEY")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET")
# Use a service account
# Link to Google Firestore Cloud Credentials
CREDENTIALS_FIREBASE_PATH = os.getenv('CREDENTIALS_FIREBASE_PATH')
FIREBASE_APIKEY = os.getenv('APIKEY')
APIKEY = os.getenv('APIKEY')
AUTH_DOMAIN = os.getenv('AUTH_DOMAIN')
DATABASE_URL = os.getenv('DATABASE_URL')
SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')
MESSAGING_SENDER_ID = os.getenv('MESSAGING_SENDER_ID')
ONESIGNAL_APP_AUTH_KEY = os.getenv('ONESIGNAL_APP_AUTH_KEY')
ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

E_MAIL_SERVER = os.getenv('MAIL_SERVER')
E_MAIL_PORT = os.getenv('MAIL_PORT')
E_MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
E_MAIL_USERNAME = os.getenv('MAIL_USERNAME')
E_MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Initialize the firebase app
try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate(CREDENTIALS_FIREBASE_PATH)
    firebase_admin.initialize_app(cred, {
        'storageBucket': STORAGE_BUCKET
    })

    bucket = storage.bucket()

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = "465",
    MAIL_USE_SSL = "True",
    MAIL_USERNAME = 'uwishuttle@gmail.com',
    MAIL_PASSWORD = '',
)

mail = Mail(app)

# Setup Session to keep user logged in
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = SECRET_KEY
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db2 = firestore.client()
fire = firestore


STUDENT_EMAIL_DOMAIN = "@mycavehill.uwi.edu"
ADMIN_EMAIL_DOMAIN = "@mycavehill.uwi.edu"
DRIVER_EMAIL_DOMAIN = "@hotmail.com"

import pyrebase

pyre_config = {
  "apiKey": FIREBASE_APIKEY,
  "authDomain": AUTH_DOMAIN,
  "databaseURL": DATABASE_URL,
  "storageBucket": STORAGE_BUCKET,
  "serviceAccount": SERVICE_ACCOUNT,
  "messagingSenderId": MESSAGING_SENDER_ID
}

pyre_firebase = pyrebase.initialize_app(pyre_config)


# Wrapper function to prevent users from requesting unauthorized pages
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# DB References
shuttle_ref = db2.collection(u'SHUTTLE_STANDS')
news_ref = db2.collection(u'NEWS')
users_ref = db2.collection(u'USERS')
logs_ref = db2.collection(u'TRIP_LOGS_TEST')
admin_logs_ref = db2.collection(u'ADMIN_LOGS')
logs_test_ref = db2.collection(u'TRIP_LOGS_TEST')

# FINAL DB
DRIVERS_REF = db2.collection(u'FINAL_USERS')
drivers_ref_list = db2.collection(u'FINAL_USERS').document(u'DRIVERS')

FINAL_TRIP_LOGS_REF = db2.collection(u'FINAL_TRIP_LOGS')
FINAL_USER_LOGS_REF = db2.collection(u'FINAL_USERS')
STUDENTS_LOGS_REF = db2.collection(u'FINAL_USERS').document(u'PASSENGERS')
FINAL_SHUTTLE_STANDS = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'EN').collection(u'CURRENT')
FINAL_SHUTTLE_STANDS_ARCHIVE = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'EN').collection(u'ARCHIVE')

# FINAL SHUTTLES FOR SPANISH
FINAL_SPANISH_SHUTTLE_STANDS = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'ES').collection(u'CURRENT')
FINAL_SPANISH_SHUTTLE_STANDS_ARCHIVE = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'ES').collection(u'ARCHIVE')

# FINAL SHUTTLES FOR FRENCH
FINAL_FRENCH_SHUTTLE_STANDS = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'FR').collection(u'CURRENT')
FINAL_FRENCH_SHUTTLE_STANDS_ARCHIVE = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'FR').collection(u'ARCHIVE')

# FINAL SHUTTLES FOR CHINESE
FINAL_CHINESE_SHUTTLE_STANDS = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'ZH').collection(u'CURRENT')
FINAL_CHINESE_SHUTTLE_STANDS_ARCHIVE = db2.collection(u'FINAL_SHUTTLE_STANDS').document(u'ZH').collection(u'ARCHIVE')

FINAL_NEWS_ALL = db2.collection(u'FINAL_NEWS').document(u'EN').collection(u'CURRENT').order_by(u'DATE', direction=firestore.Query.DESCENDING )
FINAL_NEWS = db2.collection(u'FINAL_NEWS').document(u'EN').collection(u'CURRENT')
FINAL_NEWS_TEST = db2.collection(u'FINAL_NEWS_TEST').document(u'EN').collection(u'CURRENT')
FINAL_NEWS_ARCHIVE = db2.collection(u'FINAL_NEWS').document(u'EN').collection(u'ARCHIVE')

FINAL_SPANISH_NEWS = db2.collection(u'FINAL_NEWS').document(u'ES').collection(u'CURRENT')
FINAL_SPANISH_NEWS_ARCHIVE = db2.collection(u'FINAL_NEWS').document(u'ES').collection(u'ARCHIVE')

FINAL_FRENCH_NEWS = db2.collection(u'FINAL_NEWS').document(u'FR').collection(u'CURRENT')
FINAL_FRENCH_NEWS_ARCHIVE = db2.collection(u'FINAL_NEWS').document(u'FR').collection(u'ARCHIVE')

FINAL_CHINESE_NEWS = db2.collection(u'FINAL_NEWS').document(u'ZH').collection(u'CURRENT')
FINAL_CHINESE_NEWS_ARCHIVE = db2.collection(u'FINAL_NEWS').document(u'ZH').collection(u'ARCHIVE')

# LIST OPTIONS
days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
genderOptions = ["Male", "Female", "Other"]
facultyOptions = ["Science & Technology", "Law", "Medicine", "Humanities & Education", "Social Sciences"]
levelOptions = ["Undergraduate", "Masters", "PhD"]
arrearsOptions = [True, False]
dayOptions = ["Every Day", "Monday - Friday", "Saturday - Sunday"]
intervalOptions = ["10","15","20","25","30","40", "50", "60"]
shuttleOptions = ["Campus to City","Campus to Graduate","Campus to Keith Hunte","NCF Round Trip","Warrens Round Trip"]

# List of all users
registered_users_detail = STUDENTS_LOGS_REF.get().to_dict()
registered_users = 0
arrears_registered_users = 0

for student in registered_users_detail:
    if "@mycavehill.uwi.edu" in student:
        registered_users = registered_users + 1
        if registered_users_detail[student]["ARREARS"] == True:
            arrears_registered_users = arrears_registered_users + 1

shuttles_details = FINAL_SHUTTLE_STANDS.get()
total_shuttles = 0
for shuttle in shuttles_details:
    total_shuttles = total_shuttles + 1

# Next Bus
tz = pytz.timezone('Europe/Berlin')
now = datetime.now()
day_of_week = days_of_week[now.weekday()]

# Get all shuttles running on now.weekday(), if none, next bus tomorrow
shuttle_list = shuttle_ref.get()
busAvailable = "false"
busAvailableText = ""

def checkBusAvailability():

    day = now.weekday() # get week day as number
    today = day # Keep today in mind for further comparison

    if day == 6: # If sunday reset
        day = 0
    
    day_of_week_name = days_of_week[day]

    busAvailableText = day_of_week_name

    # Loop to find the next bus
    for shuttle in shuttle_list:
        if day_of_week_name in shuttle.to_dict()["days"]:
            busAvailable = "true"
            busAvailableText = "Bus Avaiable Tomorrow"
    
    return busAvailableText


for shuttle in shuttle_list:
    if day_of_week in shuttle.to_dict()["days"]:
        busAvailable = "true"

busAvailableText = ""
if busAvailable == "false":
    busAvailableText = checkBusAvailability()
    
time_now = moment.now().strftime("%I:%M %p %A %d %B %Y")

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

# Error handlers to manage possible errors in a more user friendly way
@app.errorhandler(404)
def not_found(error):
    return render_template("error/404.html")

@app.errorhandler(405)
def not_found_405(error):
    return render_template("error/405.html")

@app.errorhandler(503)
def not_found_503(error):
    return render_template("error/503.html")

# Authentication - Login

@app.route("/login", methods=['POST','GET'])
def login():

    user = ""

    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        
        # Get the users credentials
        email = request.form['email']
        password = request.form['password']

        if email == "" and password == "":
            return render_template("login.html",error = "Please enter valid credentials") 
        
        try:

            user = verifyCredentials(email,password)
            email = user["email"]
            displayName = user["displayName"]
            token = user["idToken"]
            expire = user["expiresIn"]
            
            sessionState = setSessionInformation(email,displayName,token,expire)
            logAdminAction("LOGIN","LOGIN")
            if sessionState == "OK":
                ses = "S" #Session(app)

        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error_json = json.loads(error_json)['error']
            return render_template("login.html",error = error_json["message"].replace('_', ' ') )
        
        except requests.exceptions.Timeout as e:
            return render_template("login.html",error = "A Timeout Error Occurred" )
        
        except requests.exceptions.ConnectionError as e:
            return render_template("login.html",error = "A Connection Error Occurred" )

    return redirect(url_for('home'))


@app.route("/forgotpassword", methods=['POST','GET'])
def forgotPassword():
    if request.method == "GET":
        return render_template("forgotpassword.html")

    elif request.method == "POST":
        email = ""
    
    return redirect(url_for('login'))

def logAdminAction(action, location):

    date = datetime.now().strftime("%b %d %Y")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    user = ""
    if 'email' in session:
        user = session.get('email')

        # CHCEK IF THE DATA IS AVIALABLE
        if admin_logs_ref.document(date).get().exists:

            # Create New Shuttle Stand
            admin_logs_ref.document(date).update({
                str(timestamp) : {
                u'location': location,
                u'action': action,
                u'user': user,
                u'agent': request.headers.get('User-Agent')
                }
            })
        
        else:

            # Create New Shuttle Stand
            admin_logs_ref.document(date).set({
                str(timestamp) : {
                u'location': location,
                u'action': action,
                u'user': user
                }
            })

    return date

def setSessionInformation(email,name,token,expire):

    session['email'] = email
    session['name'] = name
    session['token'] = token
    session['expire'] = expire
    session['logged_in'] = True

    return 'OK'

def verifyCredentials(email,password):

    # Get a reference to the auth service
    auth = pyre_firebase.auth()
    user = auth.sign_in_with_email_and_password(email, password)
    return user

@app.route("/logout")
@login_required
def logout():

    session['logged_in'] = False
    session.clear()
    return home()


# Routing Pages
@app.route("/")
@login_required
def home():

    username = session['name']
    if username == "":
        username = session['email']
    
    FINAL_TRIP_LOGS = FINAL_TRIP_LOGS_REF.get()
    count = 0
    trip_count = 0
    shuttle_limit = 0
    bus_options = []

    try:

        for log_info in FINAL_TRIP_LOGS:
            
            if shuttle_limit < 3:

                pass_count = 0 
                pass_left = 0

                for m in log_info.to_dict():
                    pass_left = pass_left + int(log_info.to_dict()[m]['PASSENGERS_LEFT'])
                    pass_count = pass_count + int(log_info.to_dict()[m]['PASSENGERS_COUNT'])
                    trip_count = trip_count + 1

                shuttle_limit = shuttle_limit + 1
                bus_options.append([ log_info.id, trip_count, pass_left, pass_count, pass_count / trip_count  ])
            
    except Exception as e:
        pass

    return render_template("home.html", time  = time_now, bus_options = bus_options, username = username, registered_users = registered_users, arrears_registered_users = arrears_registered_users, total_shuttles = total_shuttles, registered_users_detail = registered_users_detail)

# Routing Functions

@app.route("/shuttles/add-shuttle", methods = ['GET', 'POST'])
def shuttles():
    form = class_form.RoutesForm()
   
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('routes/shuttles-add.html',  time  = time_now, form = form)
        else:
            return render_template('routes/routes.html')
    elif request.method == 'GET':
        return render_template('routes/shuttles-add.html',  time  = time_now, form = form)


@app.route("/routes", methods = ["GET"]) 
@login_required
def routes():
    
    # Add a new document
    shuttle_list = FINAL_SHUTTLE_STANDS.get()

    if shuttle_list:
        return render_template("routes/routes.html", time  = time_now, routes = shuttle_list)
    else:
        return render_template("routes/routes-no-data.html")

@app.route("/routes/add") 
@login_required
def routes_add():
    
    return render_template("routes/routes-add.html", time  = time_now, intervalOptions = intervalOptions)

@app.route("/routes/add-new", methods = ["POST"])
@login_required
def routes_add_new():

    if request.method == 'POST':

        name = request.form['name']
        note = request.form['notes']
        breaks = request.form['breaks']
        days = request.form['days']
        intervals = request.form['interval'] 
        description = request.form['description'] 
        start = request.form['start']
        end = request.form['end']
        times = str(start + " to " + end)

        # Translator
        translator = Translator()
        
        es_name = translator.translate(name, dest='es').text
        es_note = translator.translate(note, dest='es').text
        es_breaks = translator.translate(breaks, dest='es').text
        es_description = translator.translate(description, dest='es').text
        es_days = translator.translate(days, dest='es').text

        fr_name = translator.translate(name, dest='fr')
        fr_note = translator.translate(note, dest='fr')
        fr_breaks = translator.translate(breaks, dest='fr')
        fr_description = translator.translate(description, dest='fr')

        zh_cn_name = translator.translate(name, dest='zh-cn')
        zh_cn_note = translator.translate(note, dest='zh-cn')
        zh_cn_breaks = translator.translate(breaks, dest='zh-cn')
        zh_cn_description = translator.translate(description, dest='zh-cn')

        try:
            
             # GET GEO COORDINATES AND CREATE A FIREBASE GEO POINT
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])
            location = firestore.GeoPoint(latitude, longitude)
            
        except Exception as e:
            flash("Invalid information provided " + str(e))
            return render_template("routes/routes-add.html", intervalOptions = intervalOptions, dayOptions = dayOptions, name = name, note = note, breaks = breaks, days = days, times = times, longitude = longitude, latitude = latitude, start = start, end = end)


        if name is None or note is None or breaks is None or days is None:
            
            flash("Invalid information provided ")
            return render_template("routes/routes-add.html", intervalOptions = intervalOptions, dayOptions = dayOptions, name = name, note = note, breaks = breaks, days = days, times = times, longitude = longitude, latitude = latitude, start = start, end = end)

        else:
            
            shuttle_ref_doc = FINAL_SHUTTLE_STANDS
            shuttle_ref_doc_spanish = FINAL_SPANISH_SHUTTLE_STANDS
            shuttle_ref_doc_french = FINAL_FRENCH_SHUTTLE_STANDS
            shuttle_ref_doc_chinese = FINAL_CHINESE_SHUTTLE_STANDS

            # Create New Shuttle Stand
            new_shuttle_post_ref = shuttle_ref_doc.document().set(
            {
                u'BREAKS': breaks,
                u'DAYS': days,
                u'DESCRIPTION': description,
                u'DIRECTIONS': location,
                u'NAME': name,
                u'NOTE': note,
                u'INTERVALS': intervals,
                u'TIMES': times
            }
            )

             # Create New Spanish Shuttle Stand
            shuttle_ref_doc_spanish.document().set(
            {
                u'BREAKS': es_breaks,
                u'DAYS': es_days,
                u'DESCRIPTION': es_description,
                u'DIRECTIONS': location,
                u'NAME': es_name,
                u'NOTE': es_note,
                u'INTERVALS': intervals,
                u'TIMES': times
            }
            )
            
            logAdminAction("ADD","ROUTES")

            return redirect(url_for('routes'))
    
    return redirect(url_for('routes'))


@app.route("/routes/update/<id>")
@login_required
def routes_update(id):

    shuttle_info = FINAL_SHUTTLE_STANDS.document(id).get()
    directions_long = shuttle_info.to_dict()['DIRECTIONS'].longitude
    directions_lat = shuttle_info.to_dict()['DIRECTIONS'].latitude
    logAdminAction("VIEW","ROUTES")
    
    return render_template("routes/routes-update.html",  time  = time_now, intervalOptions = intervalOptions, longitude = directions_long, latitude = directions_lat, dayOptions=dayOptions, shuttle_info=shuttle_info, shuttle_id = id)

@app.route("/routes/update-complete/<id>",  methods = ["POST"])
@login_required
def routes_update_complete(id):

    if request.method == 'POST':

        name = request.form['name']
        note = request.form['notes']
        breaks = request.form['breaks']
        days = request.form['days']
        intervals = request.form['interval'] 
        description = request.form['description'] 
        times = str(request.form['start'] + " to " + request.form['end'])
        
        # GET GEO COORDINATES AND CREATE A FIREBASE GEO POINT
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        location = firestore.GeoPoint(latitude, longitude)

        shuttle_ref_doc = FINAL_SHUTTLE_STANDS.document(id)

        # Set the capital field
        shuttle_ref_doc.update(
            {
                u'BREAKS': breaks,
                u'DAYS': days,
                u'DESCRIPTION': description,
                u'DIRECTIONS': location,
                u'NAME': name,
                u'NOTE': note,
                u'INTERVALS': intervals,
                u'TIMES': times
            }
        )

        logAdminAction("UPDATE","ROUTES")

    flash('Form updated successfully')
    return redirect(url_for('routes'))

@app.route("/routes/delete/<id>",  methods = ["GET"])
@login_required
def routes_delete(id):

    if request.method == 'GET':

        shuttle_info = FINAL_SHUTTLE_STANDS.document(id).get()
        
        breaks = shuttle_info.to_dict()['BREAKS']
        days = shuttle_info.to_dict()['DAYS']
        description = shuttle_info.to_dict()['DESCRIPTION']
        name = shuttle_info.to_dict()['NAME']
        note = shuttle_info.to_dict()['NOTE']
        intervals = shuttle_info.to_dict()['INTERVALS']
        times = shuttle_info.to_dict()['TIMES']

        longitude = shuttle_info.to_dict()['DIRECTIONS'].longitude
        latitude = shuttle_info.to_dict()['DIRECTIONS'].latitude
        location = firestore.GeoPoint(latitude, longitude)
        
        FINAL_SHUTTLE_STANDS_ARCHIVE.document(id).set(
        {
            u'BREAKS': breaks,
            u'DAYS': days,
            u'DESCRIPTION': description,
            u'DIRECTIONS': location,
            u'NAME': name,
            u'NOTE': note,
            u'INTERVALS': intervals,
            u'TIMES': times
        })
       
        FINAL_SHUTTLE_STANDS.document(id).delete()
        logAdminAction("DELETE","ROUTES")

    flash(name + ' route removed')
    return redirect(url_for('routes'))

# Locations Functions
@app.route("/locations")   
@login_required
def locations():
    # Get a reference to the database service
    #db = firebase.database()
    # locations = db.child("LOCATIONS").get()
    locations = None

    if locations:
        return render_template("location/locations.html", data=locations)
    return render_template("location/locations-no-data.html")

# Student Functions
@app.route("/students")   
@login_required
def students():
    return render_template("student/students.html",  time  = time_now, studentList=STUDENTS_LOGS_REF.get().to_dict(), level_list = levelOptions, studentsFilteredCount = 0, studentsFiltered = [])

@app.route("/students/search", methods = ['POST'])
@login_required
def students_search():

    
    keyword = request.form['keyword']

    studentsFilteredCount = 0
    studentsFiltered = []

    students = users_ref.get()
    return render_template("student/students.html", j = "",  time  = time_now, studentList = users_ref.get(), level_list = levelOptions, keyword = keyword, studentsFilteredCount = studentsFilteredCount, studentsFiltered = studentsFiltered)


@app.route("/students/add-new",  methods = ["POST"])
@login_required
def students_add_new():

    if request.method == 'POST':
        
        name = request.form['name']
        sex = request.form['gender']
        faculty = request.form['faculty']
        level = request.form['level']
        uid = request.form['uid']
        arrears = request.form['arrears']
        
        if( arrears == "True"):
            arrears = True
        else:
            arrears = False
                
        # Document ID
        email = request.form['email'] + STUDENT_EMAIL_DOMAIN
        
        filename = "" 
        file = request.files["myFile"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_name_custom = request.form['email'] + "_" + uid + "_profile_image.jpg" 
            user_image = upload_image_file(file, file_name_custom)
            
        # Automated Feilds
        #now = datetime.now()
        #currentYear = now.year
        #qrcode = str(currentYear) + "" + str(random.randint(1,101))

        #ts = time.time()
        #timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Create New Shuttle Stand
        STUDENTS_LOGS_REF.set({
            str(u''+email) : {
                u'ARREARS': arrears,
                u'LEVEL': level,
                u'NAME': name,
                u'SEX': sex,
                u'UID': uid,
                u'IMAGE_URL': user_image,
                u'FACULTY': faculty
            }
        }, merge=True)
        
        logAdminAction("ADD","STUDENTS")

        return redirect(url_for('students'))
    
@app.route("/students/add")
def students_add():
    return render_template("student/students-add.html", time  = time_now)

@app.route("/students/update/<id>") 
@login_required
def students_update(id):

    # GET TRIP LOGS FOR THIS STUDENT
    FINAL_TRIP_LOGS = FINAL_TRIP_LOGS_REF.get()
    count = 0
    trip_count = 0
    bus_options = []

    try:

        for log_info in FINAL_TRIP_LOGS:
            for m in log_info.to_dict():
                if id in log_info.to_dict()[m]['PASSENGERS']:
                    trip_count = trip_count + 1
            bus_options.append([ log_info.id, trip_count ])
            
    except Exception as e:
        pass
    
        
    student_info = STUDENTS_LOGS_REF.get().to_dict()
    for i in student_info:
        if i == id:
            return render_template("student/students-update.html",  time  = time_now,student_info = student_info[i], studentid = id, genderOptions = genderOptions, facultyOptions= facultyOptions, levelOptions= levelOptions, bus_options= bus_options)


    logAdminAction("VIEW","STUDENTS")
    return render_template("student/students.html",  time  = time_now, student_info = student_info, studentid = id, genderOptions = genderOptions, facultyOptions= facultyOptions, levelOptions= levelOptions)



@app.route("/students/update-complete/<id>",  methods = ["POST"])
@login_required
def students_update_complete(id):

    name = request.form['name']
    sex = request.form['sex']
    faculty = request.form['faculty']
    level = request.form['level']
    uid = request.form['uid']
    email = request.form['email'] + STUDENT_EMAIL_DOMAIN # Document ID

    arrears = request.form['arrears']
    if( arrears == "True"):
        arrears = True
    else:
        arrears = False
    
    student_ref_doc = users_ref.document(id)

    # Set the capital field
    STUDENTS_LOGS_REF.set({
        str(u''+id) : {
            u'NAME': name,
            u'FACULTY': faculty,
            u'SEX': sex,
            u'LEVEL': level,
            u'UID': uid,
            u'ARREARS': arrears
        }
    }, merge=True)

    logAdminAction("UPDATE","STUDENTS")
    flash( name + ' Profile Information Updated Successfully ')
    return redirect(url_for('students_update', id = id ))

@app.route("/students/update-complete-image/<id>",  methods = ["POST"])
@login_required
def students_update_complete_image(id):

    file = request.files["profile_image"]

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        file_name_custom = id.rsplit('@')[0] + "_profile_image.jpg" 
        user_image = upload_image_file(file, file_name_custom)

        student_ref_doc = users_ref.document(id)

        # Set the capital field
        STUDENTS_LOGS_REF.set({
            str(u''+id) : {
                u'IMAGE_URL': user_image
            }
        }, merge=True)
        
    logAdminAction("UPDATE","STUDENTS")
    flash('Profile Image Updated Successfully ')
    return redirect(url_for('students_update', id = id)) 

# Drivers Functions
@app.route("/driver")   
@login_required
def drivers():

    # Get a reference to the database service
    #db = firebase.database()
    #users = db.child("USERS").get()
    

    # Add a new document
    driversList = drivers_ref_list.get().to_dict()

    for i in driversList:
        driver_user = auth.get_user_by_email(i)

        disable_status = driver_user.disabled
        if disable_status == True:
            driversList[i]['DISABLED_TEXT'] = "Enable"
        else:
            driversList[i]['DISABLED_TEXT'] = "Disable"

        driversList[i]['DISABLED'] = driver_user.disabled
        driversList[i]['UID'] = driver_user.uid
        driversList[i]['PHONE'] = driver_user.phone_number

    return render_template("driver/drivers.html",  time  = time_now, driversList = driversList)

@app.route("/driver/add-new",  methods = ["POST","GET"])
@login_required
def drivers_add_new():

    form = class_form.DriverForm()

    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email'] + "@hotmail.com"
        phone = request.form['telephone']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        try:
            
            # Add driver to driver list in users
            user = auth.create_user(
                email=email,
                email_verified=False,
                phone_number=phone,
                password=password,
                display_name=name,
                disabled=False
            )

            link = ""

        except Exception as e:
            flash('There was an error adding the driver. ' + str(e) )
            return render_template("driver/driver-add.html", time  = time_now, form = form)

        try:
            
            # Add driver to driver list in users
            DRIVERS_REF.document(u'DRIVERS').set({
                str(u''+email) : {
                    u'NAME': name,
                }
            }, merge=True)


        except Exception as e:
            flash('There was an error adding the driver to the driver table: details ' + str(e) )
            return render_template("driver/driver-add.html", time  = time_now, form = form)
        
        logAdminAction("ADD","DRIVERS")
        return redirect(url_for('drivers'))
    
    elif request.method == 'GET':
        return redirect(url_for('driver_add'))


@app.route("/driver/enable/<id>",  methods = ["GET"])
@login_required
def drivers_enable(id):

    try:

        user = auth.update_user(
        id,
        disabled=False)
        
    except Exception as e:

        flash('An error occured.' + str(e))
        return redirect(url_for('drivers'))
    
    logAdminAction("ENABLE " + id,"DRIVERS")
    return redirect(url_for('drivers'))

@app.route("/driver/disable/<id>",  methods = ["GET"])
@login_required
def drivers_disable(id):

    try:

        user = auth.update_user(
        id,
        disabled=True)
        
    except Exception as e:

        flash('An error occured.' + str(e))
        return redirect(url_for('drivers'))
        
    logAdminAction("DISABLE " + id,"DRIVERS")
    return redirect(url_for('drivers'))

@app.route("/driver/add")
def driver_add():
    form = class_form.DriverForm()
    return render_template("driver/driver-add.html", time  = time_now, form = form)

# Not Implemented
@app.route("/driver/update/<id>") 
@login_required
def driver_update(id):

    student_info = users_ref.document(id).get()

    checkInArrears = False
    checkIsRegistered = False

    inarrears = student_info.to_dict()['arrears']
    if inarrears == True:
        checkInArrears = True

    isregistered = True #student_info.to_dict()['registered']
    if isregistered == True:
        checkIsRegistered = True

    logAdminAction("VIEW","DRIVER")
    return render_template("driver/driver-update.html", student_info = student_info, studentid = id, genderOptions = genderOptions, facultyOptions= facultyOptions, levelOptions= levelOptions)

# Not Implemented
@app.route("/driver/update-complete/<id>",  methods = ["POST"])
@login_required
def driver_update_complete(id):

    name = request.form['name']
    gender = request.form['gender']
    faculty = request.form['faculty']
    level = request.form['level']
    studentid = request.form['studentid']

    arrears = request.form['arrears']
    if( arrears == "True"):
        arrears = True
    else:
        arrears = False
    
    registered = request.form['registered']
    if( registered == "True"):
        registered = True
    else:
        registered = False

    # Document ID
    email = request.form['email'] + "@hotmail.com"
    
    student_ref_doc = users_ref.document(id)

    # Set the capital field
    student_ref_doc.update(
        {
            u'name': name,
            u'gender': gender,
            u'faculty': faculty,
            u'level': level,
            u'studentid': studentid,
            u'arrears': arrears,
            u'registered': registered
        }
    )

    logAdminAction("UPDATE","DRIVER")
    return redirect(url_for('drivers'))

#################################################################################
########################### News & Alerts ######################################
########################### News & Alerts Functions ############################
#################################################################################

@app.route("/news", methods = ["GET"]) 
@login_required
def news():
    if news is not None:
        return render_template("news/news.html",time = time_now, newsArticles = FINAL_NEWS_ALL.get(), keyword = "", newsFilteredCount = 0, newsFiltered = "")
    else:
        return render_template("news/news-no-data.html",time = time_now)

@app.route("/news/search", methods = ['POST'])
@login_required
def news_search():

    news = FINAL_NEWS.get()
    keyword = request.form['keyword']

    newsFilteredCount = 0
    newsFiltered = []
    if news:
        for content in news:
            if content.to_dict()["TITLE"].lower().find(keyword.lower() ) != -1:
                newsFiltered.append( [content.id, content.to_dict()] )
                newsFilteredCount = newsFilteredCount + 1

    logAdminAction("SEARCH","NEWS")
    return render_template("news/news.html", time = time_now, newsArticles = FINAL_NEWS.get(), keyword = keyword, newsFilteredCount = newsFilteredCount, newsFiltered = newsFiltered)

@app.route("/news/add", methods = ['GET', 'POST'])
@login_required
def news_add():
    #db = firebase.database()
    #news = None #db.child("NEWS").get()

    if request.method == 'POST':
        
        name = request.form['news_name']
        description = request.form['description']
        date = datetime.now()

        expires = datetime.strptime(request.form['expires'] + '  1:00PM', '%d/%m/%Y %I:%M%p')

        translator = Translator()
        
        es_name = translator.translate(name, dest='es').text
        es_description = translator.translate(description, dest='es').text

        fr_name = translator.translate(name, dest='fr').text
        fr_description = translator.translate(description, dest='fr').text

        zh_cn_name = translator.translate(name, dest='zh-cn').text
        zh_cn_description = translator.translate(description, dest='zh-cn').text

        #Save Information
        FINAL_NEWS.document().set({
            u'TITLE': name,
            u'DESCRIPTION': description,
            u'DATE': date,
            u'EXPIRY_DATE': expires,
        })

        #news_id = news_id_ref.key()

        # Implement other languages
        FINAL_SPANISH_NEWS.document().set({
            u'TITLE': es_name,
            u'DESCRIPTION': es_description,
            u'DATE': date,
            u'EXPIRY_DATE': expires,
        })

        # Implement other languages
        FINAL_FRENCH_NEWS.document().set({
            u'TITLE': fr_name,
            u'DESCRIPTION': fr_description,
            u'DATE': date,
            u'EXPIRY_DATE': expires,
        })

        # Implement other languages
        FINAL_CHINESE_NEWS.document().set({
            u'TITLE': zh_cn_name,
            u'DESCRIPTION': zh_cn_description,
            u'DATE': date,
            u'EXPIRY_DATE': expires,
        })

        jsonResponse = sendUserNotification(name, description)
        
        logAdminAction("ADD","NEWS")

        flash('Notification Send Successfully')
        return redirect(url_for('news'))
    else:
        return render_template("news/news-add.html", time = time_now, error = "")

def sendUserNotification(name, description):

    # Create a onesignal client
    onesignal_client = onesignal_sdk.Client(app_auth_key=ONESIGNAL_APP_AUTH_KEY, app_id=ONESIGNAL_APP_ID)

    # create a notification
    new_notification = onesignal_sdk.Notification(post_body={
        "headings": {"en": name},
        "contents": {"en": description}
    })

    new_notification.post_body["content"] = {"en": description}
    #new_notification.post_body["data"] = {"foo": 123, "bar": "foo"}
    new_notification.post_body["included_segments"] = ["Active Users", "Inactive Users"]

    # send notification, it will return a response
    onesignal_response = onesignal_client.send_notification(new_notification)

    json = onesignal_response.json()
    return json


@app.route("/news/update/<id>",  methods = ["GET"])
@login_required
def news_update(id):

    news_ref_doc = FINAL_NEWS.document(id).get()
    form = class_form.NewsForm()
    logAdminAction("VIEW","NEWS")
    return render_template("news/news-update.html", time = time_now, news_info = news_ref_doc, form = form)

@app.route("/news/delete/<id>",  methods = ["GET"])
@login_required
def news_delete(id):

    if request.method == 'GET':
        
        logAdminAction("DELETE","NEWS")
        news_ref.document(id).delete()

    return redirect(url_for('news'))

# Admin Functions
@app.route("/admin")
def admin():
    # Add a new document
    students = users_ref.get()
    # Start listing users from the beginning, 1000 at a time.
    page = auth.list_users()
    userslist = []

    for user in page.users:
        if 'mycavehill' not in user.email:
            userslist.append({ "display_name":str(user.display_name), "email":user.email, "uid":user.uid })
    
    return render_template("admin/admin.html" , time = time_now, adminUsers=page, adminus = userslist)

@app.route("/admin/add", methods = ['GET', 'POST'])
def admin_user_add():

    form = class_form.AdminUserForm()

    if request.method == 'POST':

        if form.validate():

            name = request.form['name']
            email = request.form['email']
            phone = request.form['telephone']
            password = request.form['password']
            confirmpassword = request.form['confirmpassword']

            try:
                user = auth.create_user(
                    email=email,
                    email_verified=False,
                    phone_number=phone,
                    password=password,
                    display_name=name,
                    disabled=False
                )

                link = ""

                #action_code_settings = auth.ActionCodeSettings(
                #    dynamic_link_domain='coolapp.page.link',
                #)

                #link = auth.generate_email_verification_link(email, action_code_settings)

                #send_custom_email(email, link)

            except Exception as e:
                flash('There was an error creating the user ' + str(e) )
                return render_template("admin/admin-add.html", form = form)
            

            # 
            # Construct email from a template embedding the link, and send
            # using a custom SMTP server.
            # send_custom_email(email, link)

            if user.uid:
                flash('We have sent ' + name + " an email to verify their account at " + email + " " + link)
                return redirect(url_for("admin"))
            else:
                flash('There was an error creating the user')
                return render_template("admin/admin-add.html", form = form)
        else: 
            return render_template("admin/admin-add.html", time = time_now, form = form)
    else:

        return render_template("admin/admin-add.html", time = time_now, form = form)

@app.route("/admin/update_photo/<id>", methods = ['POST'])
def admin_user_update_photo(id):

    form = class_form.AdminUpdateForm()
    user = auth.get_user(id)

    try:
                
        filename = "" 
        file = request.files["myFile"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            file_name_custom = id + "_profile_image.jpg" 
            user_image = upload_image_file(file, file_name_custom)

            
    except Exception as e:
        flash('An error occured.' + str(e))
        return render_template('admin/admin-update.html', form = form, admin_info = user, adminID = id) 

    try:
        
        user = auth.update_user(
        id,
        photo_url=user_image)
        
    except Exception as e:

        flash('An error occured.' + str(e))
        return render_template('admin/admin-update.html', form = form, admin_info = user, adminID = id) 
    
    
    return redirect(url_for("admin"))

@app.route("/admin/update/<id>", methods = ['GET', 'POST'])
def admin_user_update(id):

    #uid = "MI1NkW8gziQBAPwLC1RdLNqBH9E2"
    user = auth.get_user(id)
    
    form = class_form.AdminUpdateForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.' + str(form.errors))
            return render_template('admin/admin-update.html', form = form, admin_info = user, adminID = id)
        else:

            #Update user information
            name = request.form['name']
            email = request.form['email']
            telephone = request.form['telephone']

            try:
                
                user = auth.update_user(
                id,
                display_name=name,
                phone_number=telephone)
                
                return redirect(url_for("admin"))

            except Exception as e:

                flash('An error occured.' + str(e))
                return render_template('admin/admin-update.html', form = form, admin_info = user, adminID = id) 
           
    elif request.method == 'GET':
        return render_template('admin/admin-update.html', form = form, admin_info = user, adminID = id)

def upload_image_file(file, custom_file_name):

    path = '/uwi-shuttle-user-id.appspot.com/'+str(secure_filename(file.filename))
    if file: 
        try:
            bucket = storage.bucket()
            #file is just an object from request.files e.g. file = request.files['myFile']
            URL = os.getcwd() + "/" + UPLOAD_FOLDER + "/" + file.filename
            blob = bucket.blob("user_profile_pictures/" + custom_file_name)
            blob.upload_from_filename(URL)

            url = blob.generate_signed_url(
            # This URL is valid for 1 hour
            expiration=timedelta(hours=60),
            # Allow GET requests using this URL.
            method='GET')
            
            return url
            
        except Exception as e:
            return 'error uploading user photo: ' + str(e) + " " + URL

@app.route("/admin/update-complete/<id>", methods = ["POST"])
def admin_user_update_complete(id):

    #uid = "MI1NkW8gziQBAPwLC1RdLNqBH9E2"

    #user = auth.update_user(
    #uid,
    #email='romariorenee@gmail.com',
    #phone_number='+15555550100',
    #email_verified=True,
    #password='someTrashPassword',
    #display_name='Romario Doe',
    #photo_url='https://randomuser.me/api/portraits/men/25.jpg',
    #disabled=False)
    
    #return 'Sucessfully updated user: {0}'.format(user.uid)

    if request.method == 'POST':
        
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        disabled = request.form.getlist('disabled')

    return id

@app.route("/admin/admin-delete")
def admin_user_delete():
    return render_template("admin/admin-delete.html")

@app.route("/insights") 
def insights():

    log_ref = db2.collection(u'TRIPS_LOGS').get()
    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    
    FINAL_TRIP_LOGS = FINAL_TRIP_LOGS_REF.get()
    count = 0
    trip_count = 0
    shuttle_limit = 0
    bus_options = []
    bus_options_chart = []
    bus_options_chart_labels = []

    try:

        for log_info in FINAL_TRIP_LOGS:
        
            pass_count = 0 
            pass_left = 0
            chart_deep_details = []

            for m in log_info.to_dict():
                pass_left = pass_left + int(log_info.to_dict()[m]['PASSENGERS_LEFT'])
                pass_count = pass_count + int(log_info.to_dict()[m]['PASSENGERS_COUNT'])
                trip_count = trip_count + 1
                chart_deep_details.append([m,pass_count])

            bus_options_chart_labels.append([log_info.id])
            bus_options_chart.append([ trip_count])
            bus_options.append([ log_info.id, trip_count, pass_left, pass_count, pass_count / trip_count  ])
        
    except Exception as e:
        pass

    # Get test data
    logs_test = logs_ref.get() 
    shuttle_list = logs_test

    logAdminAction("VIEW","INSIGHTS")
    return render_template("insights/insights.html", labels = bus_options_chart_labels, values = bus_options_chart, total_shuttles = total_shuttles, logs = log_ref,time  = time_now, busAvailableText = busAvailableText, shuttle_list = shuttle_list, registered_users = registered_users, arrears_registered_users = arrears_registered_users, registered_users_detail = registered_users_detail, bus_options = bus_options)


@app.route("/charts")
def chart():


    return render_template('chart.html')

@app.route('/get_chart_data')
def get_chart_data():

    FINAL_TRIP_LOGS = FINAL_TRIP_LOGS_REF.get()
    count = 0
    trip_count = 0
    bus_options_chart = []
    bus_options_chart_labels = []

    for log_info in FINAL_TRIP_LOGS:
    
        pass_count = 0 
        pass_left = 0
        chart_deep_details = []

        for m in log_info.to_dict():
            pass_left = pass_left + int(log_info.to_dict()[m]['PASSENGERS_LEFT'])
            pass_count = pass_count + int(log_info.to_dict()[m]['PASSENGERS_COUNT'])
            trip_count = trip_count + 1
            chart_deep_details.append([m,pass_count])

        bus_options_chart_labels.append(log_info.id)
        bus_options_chart.append(trip_count)

    labels = bus_options_chart_labels
    data = bus_options_chart

    return jsonify({'payload':json.dumps({'data':data, 'labels':labels})})

@app.route("/logs") 
def admin_change_logs():

    # Get Log Data
    logs_arr = []
    date = datetime.now().strftime("%b %d %Y")
    logs = admin_logs_ref.get()

    return render_template("admin/logs.html",time  = time_now , logs2 = admin_logs_ref.get() )

@app.route("/simulate") 
def admin_simulate():

    return render_template("admin/simulate.html",time  = time_now)

@app.route("/simulate_driver") 
def admin_simulate_driver():

    logAdminAction("RUN","SIMULATE DRIVERS")
    fake = Faker()
    DRIVER_ENTRIES = 2
    m = 0

    while m < DRIVER_ENTRIES:
        
        
        fakeUser = fake.profile(fields=None, sex=None)
        fullname = fakeUser["name"]
        email = fullname.replace(" ", "").lower() + DRIVER_EMAIL_DOMAIN
        #image = fakeUser["name"]
        phone = "+1246" + str( random.randint(2145623,2945623) )
        gender = fakeUser["sex"]
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        try:
            user = auth.create_user(
                email=email,
                email_verified=False,
                phone_number=phone,
                password=password,
                display_name=fullname,
                disabled=False
            )

        except Exception as e:
            flash('There was an error creating the user ' + str(e) )
            return render_template("admin/simulate.html",time  = time_now)
            
        # Add driver to driver list in users
        DRIVERS_REF.document(u'DRIVERS').set({
            str(u''+email) : {
                u'NAME': fullname,
            }
        }, merge=True)

        m = m + 1

    return redirect(url_for('drivers'))


@app.route("/simulate_logs") 
def admin_simulate_logs():

    logAdminAction("RUN","SIMULATE TRIP LOGS")

    LOG_ENTRIES = 2
    m = 0

    # GET ALL DRIVERS AND STORE THEM INTO A LIST OF JUST EMAIL
    driversList = drivers_ref_list.get().to_dict()
    DRIVERS_EMAIL_LIST = []
    driver_list_count = 0

    for i in driversList:
        DRIVERS_EMAIL_LIST.append(i)
        driver_list_count = driver_list_count + 1
    driver_list_count = driver_list_count - 1

    # GET ALL STUDENTS AND STORE THEM INTO A LIST OF JUST EMAIL
    passengersList = STUDENTS_LOGS_REF.get().to_dict()
    PASSENGERS_EMAIL_LIST = []
    passenger_list_count = 0

    for n in passengersList:
        if n != "DATABASE_AVAILABLE":
            PASSENGERS_EMAIL_LIST.append(n)
            passenger_list_count = passenger_list_count + 1
    passenger_list_count = passenger_list_count - 1

    while m < LOG_ENTRIES:

        shuttle = shuttleOptions[random.randint(0,4)]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        PASSENGERS_COUNT = random.randint(0,10)
        PASSENGERS_LEFT = random.randint(0,10)
        TIMESTAMP = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # GET A RANDOM DRIVER
        DRIVER_EMAIL = DRIVERS_EMAIL_LIST[random.randint(0,driver_list_count)]
            
        # GET PASSENGERS
        l = 0
        PASSENGERS_LIST_ONBOARD = []
        while l < PASSENGERS_COUNT:

            PERSON = PASSENGERS_EMAIL_LIST[random.randint(0,passenger_list_count)]
            if PERSON not in PASSENGERS_LIST_ONBOARD:
                PASSENGERS_LIST_ONBOARD.append(PERSON)
        l = l + 1

        FINAL_TRIP_LOGS_REF.document(shuttle).set({
            str(u''+timestamp) : {
                u'DRIVER_EMAIL': DRIVER_EMAIL,
                u'PASSENGERS': PASSENGERS_LIST_ONBOARD,
                u'PASSENGERS_COUNT': PASSENGERS_COUNT,
                u'PASSENGERS_LEFT': PASSENGERS_LEFT,
                u'TIMESTAMP': timestamp
            }
        }, merge=True)

    m = m + 1

    return redirect(url_for('students'))

@app.route("/simulate_students") 
def admin_simulate_students():

    logAdminAction("RUN","SIMULATE DRIVERS")
    fake = Faker()
    STUDENT_ENTRIES = 10
    m = 0

    while m < STUDENT_ENTRIES:
        
        uid = random.randint(123456,199999)
        fakeUser = fake.profile(fields=None, sex=None)
        fullname = fakeUser["name"]
        email = fullname.replace(" ", "").lower() + STUDENT_EMAIL_DOMAIN
        #image = fakeUser["name"]
        phone = "+1246" + str( random.randint(2145623,2945623) )
        sex = fakeUser["sex"]
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        level = levelOptions[random.randint(0,1)]
        arrears = arrearsOptions[random.randint(0,1)]
        faculty = facultyOptions[random.randint(0,4)]

        user_id_for_image = str(random.randint(1,101))

        sexType = "women"
        if sex == "Male":
            sexType = "men"

        user_image = "https://randomuser.me/api/portraits/"+ sexType +"/"+ user_id_for_image +".jpg"
        
        try:
            user = auth.create_user(
                email=email,
                email_verified=True,
                phone_number=phone,
                password=password,
                display_name=fullname,
                disabled=False
            )

        except Exception as e:
            flash('There was an error creating the student ' + str(e) )
            return render_template("admin/simulate.html")
            
        # Add student to student list in users
        STUDENTS_LOGS_REF.set({
            str(u''+email) : {
                u'NAME': fullname,
                u'SEX': sex,
                u'FACULTY': faculty,
                u'LEVEL': level,
                u'IMAGE_URL': user_image,
                u'UID': uid,
                u'ARREARS': arrears
            }
        }, merge=True)

        m = m + 1

    return redirect(url_for('students'))

@app.route("/simulate_students_old") 
def admin_simulate_students_old():

    logAdminAction("RUN","SIMULATE")

    # Used for Fake Data

    fake = Faker()

    # Get Log Data
    logs_arr = []
    logs = admin_logs_ref.get()

    FINAL_TRIP_LOGS = FINAL_TRIP_LOGS_REF.get()

    counter = 0
    logsTest = []
    logs = []

    # GENERATE DRIVERS
    DRIVER_ENTRIES = 2

    fakeUser = fake.profile(fields=None, sex=None)

    fullname = fake.name()
    email = fake.email()
    image = fake.image_url()
    phone = fake.phone_number()
    #gender = fake.sex()

    m = 0
    while m < DRIVER_ENTRIES:
        
        # Add driver to driver list in users
        DRIVERS_REF.document(u'DRIVERS').set({
            str(u''+email) : {
                u'NAME': fullname,
            }
        }, merge=True)

        m = m + 1

    # Fetching the data from the database and restructuring it into our own custom object
    for log_info in FINAL_TRIP_LOGS:
        logs = [log_info.id,log_info]
        logsTest.append({"ID":log_info.id, "PASSENGERS_LEFT":0, "PASSENGERS_COUNT": 0, "PASSENGERS": [], "DRIVER_EMAIL":""})
        counter = counter + 1
        for m in log_info.to_dict():
            logsTest[counter-1]["PASSENGERS_LEFT"] = log_info.to_dict()[m]['PASSENGERS_LEFT']
            logsTest[counter-1]["PASSENGERS_COUNT"] = log_info.to_dict()[m]['PASSENGERS_COUNT']
            logsTest[counter-1]["PASSENGERS"] = log_info.to_dict()[m]['PASSENGERS']
            logsTest[counter-1]["DRIVER_EMAIL"] = log_info.to_dict()[m]['DRIVER_EMAIL']
    
    # Create our object and save to the database
    TRIP_LOG_ENTRIES = 20
    passengers = [0,24]
    drivers = 5
    passengersLeft_options = [0,15]
    shuttle_service = ["Campus to City","Campus to Graduate","Campus to Keith Hunte","NCF Round Trip","Warrens Round Trip"]

    i = 0
    while i < TRIP_LOG_ENTRIES:

        # Create document for a shuttle service
        service_name = shuttle_service[0]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        driver_email = "nigel@mycavehill.uwi.edu"
        passengers_list = ["romariorenee@mycavehill.uwi.edu"]
        passengers_count = len(passengers_list)
        passengers_left = passengersLeft_options[0]

        logs_test_ref.document(service_name).update({
            str(timestamp) : {
            u'DRIVER_EMAIL': driver_email,
            u'PASSENGERS': passengers_list,
            u'PASSENGERS_COUNT': passengers_count,
            u'PASSENGERS_LEFT': passengers_left
            }
        })

        i = i + 1

    #return FINAL_TRIP_LOGS

    # Create Two Semesters Worth of Content
    # 5 Months
    # 5 Days Per Week

    return render_template("admin/simulate.html", logs = logs, logs2 = logsTest )

@app.route("/mail", methods=['POST','GET'])
def sendMail():

    form = class_form.ContactForm()

    if request.method == "GET":
        return render_template("admin/contact.html",time  = time_now, form = form)

    elif request.method == "POST":
        
        if form.validate():

            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']

            msg = Message("New Message from UWI Service",
                sender="uwishuttle@gmail.com",
                recipients=["romariorenee@gmail.com", email],
                body=" just sent you a message. Please see the information below. " )

            mail.send(msg)

            flash('Message Sent: ' + str(msg))
            return render_template("admin/contact.html",time  = time_now, form = form)
        
        else:

            flash('Please enter all of the information required below' + str(form.errors))
            return render_template("admin/contact.html",time  = time_now, form = form)
    

@app.route("/about") 
@login_required
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)