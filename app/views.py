from app import app, mongo

from flask import render_template, request, url_for, redirect, flash, session

from werkzeug.utils import secure_filename

from flask import send_from_directory, abort

from flask_mongoengine import MongoEngine

import bson.binary

import urllib.request

import os, re

import datetime

from functools import wraps

# app.config = os.urandom(24)

app.config["SECRET_KEY"] = "b'n\x1d\xb1\x8a\xc0Jg\x1d\x08|!F3\x04P\xbf'"

# app.config["MONGODB_SETTINGS"] = {
#     'db': 'SIS',
#     'host': 'localhost',
#     'port': 27017   
# }

# db = MongoEngine()
# db.init_app(app)

app.config["UPLOAD_FOLDER"] = "D:/CSI FYP Works/Julius's work/Pet finding app/app/static/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["TXT", "DOC", "PNG", "JPG", "JPEG", "GIF"]
app.config["CLIENT_IMAGES"] = "/Users/Anyiglobal/Desktop/MyProject/app/static/img/clients"

def nigerian_time():
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    today = datetime.date.today()
    d2 = today.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S %p")
    return (d2 +' '+'at'+' '+tm)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", 'danger')
            return redirect(url_for("index"))
    return wrap

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You are successfully logged out!", 'success')
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/register")
def register():
    return render_template("public/register.html")

@app.route("/students/dashboard")
@login_required
def students_dashboard():
    return render_template("public/students_portal.html")

@app.route("/add-missing-pet", methods=['GET', 'POST'])
@login_required
def add_missing_pet():
    if request.method=='POST':
        req = request.form
        
        ownersname = req["ownersName"]
        ownersemail = req["ownersEmail"]
        ownersphoneno = req["ownersPhoneNumber"]
        petname = req["petName"]
        petcolor = req["petColor"]
        pettype = req["petType"]
        gender = req["gender"]
        petage = req["petAge"]
        
        mongo.db.missingPets.insert_one({"Owner's Name": ownersname, "Owner's Email": ownersemail, "Owner's Phone Number": ownersphoneno, "Pet Name": petname, "Pet Color": petcolor, "Pet Type": pettype, "Gender": gender, "Pet Age": petage})
        
        flash("Record Added Successfully!", "success")
        return redirect(url_for("add_missing_pet"))
        
    return render_template("public/add_missing_pet.html")

@app.route("/all-pets-found")
@login_required
def all_pets_found():
    return render_template("public/all_pets_found.html")

@app.route("/lecturers-profile")
@login_required
def lecturers_profile():
    return render_template("public/lecturers_profile.html")

@app.route("/student-profile")
@login_required
def student_profile():
    return render_template("public/student_profile.html")

# Allowed files to be uploaded
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in app.config["ALLOWED_EXTENSIONS"]

@app.route('/upload-pet-image', methods=["GET", "POST"])
@login_required
def upload_pet_image():
    if request.method=='POST':
        if 'file' not in request.files:
            flash("No file part!", 'warning')
            return render_template("public/upload_pet_image.html")
        file = request.files['file']
        if file.filename=='':
            flash("No selected file, please select a file", 'warning')
            return render_template("public/upload_pet_image.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)   
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("File uploaded successfully", 'success')
            return render_template("public/upload_pet_image.html")
    return render_template("public/upload_pet_image.html")

@app.route("/sign-up", methods=["GET", "POST"])
@login_required
def sign_up():
    if request.method=='POST':
        req = request.form
        
        username = str(req["username"])
        email = str(req["email"]).lower()
        password = req["pswd"]
        con_password = req["con_pswd"]
        
        # matric_number = mat_no.split('/')
        
        if password != con_password:
            flash("Password Confirmation Mismatched, Please Confirm Your Password!", "danger")
            return render_template("public/register.html")
        # checkuser = mongo.db.sign_up.find_one({"matric_number":mat_no}, {"_id":0})
        checkuser = mongo.db.signup.find_one({username:{"$exists":True}}, {"_id":0})
        if checkuser:
            flash("Sorry, User already registered!", "danger")
            return render_template("public/register.html")
        # checkemail = mongo.db.sign_up.find_one({"email":email}, {"_id":0})
        checkemail = mongo.db.signup.find_one({email:{"$exists":True}}, {"_id":0})
        if checkemail:
            flash("Sorry, User with email address already exists!", "danger")
            return render_template("public/register.html")
        
        mongo.db.signup.insert_one({"username": username, username:username, "email": email, email:email, "password": password, "activationStatus":"0", "registeredDate": nigerian_time()})
        flash("Account Created Successfully!", "success")
        return redirect(url_for("index"))
    else:
        return render_template("public/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='POST':
        req = request.form
        
        username = str(req["username"])
        pswd = req["pswd"]
        
        # checkuser = mongo.db.sign_up.find_one({"matric_number": mat_no})
        checkuser = mongo.db.signup.find_one({username:{"$exists":True}}, {"_id":0})
        
        # x = re.search(pattern, string)
        
        if not checkuser:
            flash("Username/Password Incorrect!", "danger")
            return render_template("public/index.html")
        
        elif checkuser["activationStatus"] != "1":
            flash("Account not activated. Contact Admin for account activation!", "danger")
            return render_template("public/index.html")
        
        elif not pswd == checkuser["password"]:
            flash("Username/Password Incorrect!", "danger")
            return render_template("public/index.html")
                  
        else:
            del checkuser["password"]
            session["user"] = checkuser
            session["login"]=True
            if checkuser["username"] == "admin":
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for("admin_dashboard"))
            
            else:
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for("students_dashboard"))
    
    return render_template("public/index.html")

        
@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method=='POST':
        req = request.form
        print(req)
    
        username = req["username"]
        new_email = req["email"]
    
        # checkuser = mongo.db.sign_up.find_one({"matric_number":mat_no}, {"_id":0})
        checkuser = mongo.db.signup.find_one({username:{"$exists":True}}, {"_id":0})
        if not checkuser:
            flash("Sorry, User not registered!", "danger")
            return render_template("public/student_profile.html")
        # checkemail = mongo.db.sign_up.find_one({"email":email}, {"_id":0})
        checkemail = mongo.db.signup.find_one({new_email:{"$exists":True}}, {"_id":0})
        if checkemail:
            flash("Sorry, User with email address already exists!", "danger")
            return render_template("public/student_profile.html")
    
        old_email = checkuser["email"]
        # mongo.db.sign_up.update_one({mat_no:{"$exists":True}}, {"$unset": {"email": old_email,:new_email}})
        mongo.db.signup.update_one({username:{"$exists":True}}, {"$set": {"email": new_email}, "$unset": {old_email: ""}})
        flash("Profile Updated Successfully!", "success")
        return redirect(url_for("student_profile"))
    
    return render_template("public/student_profile.html")

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method=='POST':
        req = request.form
    
        currentpswd = req["currentpassword"]
        newpswd = req["newpassword"]
        renewpswd = req["renewpassword"]
    
        # checkuser = mongo.db.sign_up.find_one({"matric_number":mat_no}, {"_id":0})
        checkpassword = mongo.db.signup.find_one({currentpswd:{"$exists":True}}, {"_id":0})
        if not checkpassword:
            flash("Sorry, Incorrect Password", "danger")
            return render_template("public/student_profile.html")
        # checkemail = mongo.db.sign_up.find_one({"email":email}, {"_id":0})
        if newpswd == currentpswd:
            flash("Sorry, Current password and New password must be different!", "danger")
            return render_template("public/student_profile.html")
        if newpswd != renewpswd:
            flash("New password do not match!", "danger")
            return render_template("public/student_profile.html")
        # checkemail = mongo.db.signup.find_one({new_email:{"$exists":True}}, {"_id":0})
        # if checkemail:
        #     flash("Sorry, User with email address already exists!", "danger")
        #     return render_template("public/student_profile.html")
        
        old_pswd = checkpassword['password']
        # mongo.db.sign_up.update_one({mat_no:{"$exists":True}}, {"$unset": {"email": old_email,:new_email}})
        mongo.db.signup.update_one({currentpswd:{"$exists":True}}, {"$set": {"password": newpswd}, "$unset": {old_pswd: ""}})
        flash("Password Changed Successfully!", "success")
        return redirect(url_for("student_profile"))
    
    return render_template("public/student_profile.html")