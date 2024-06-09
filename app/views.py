from app import app, mongo

from flask import jsonify, render_template, request, url_for, redirect, flash, session

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

@app.route("/supervisor/dashboard")
@login_required
def supervisor_dashboard():
    return render_template("public/supervisor_portal.html")

@app.route("/add-student-info", methods=['GET', 'POST'])
@login_required
def add_student_info():
    if request.method=='POST':
        req = request.form
        
        name = req["name"]
        matric_no = req["matric_no"]
        faculty = req["faculty"]
        course_of_study = req["course"]
        year_of_study = req["year"]
        perm_address = req["address"]
        sex = req["sex"]
        name_of_sup = req["name_of_sup"]
        name_of_cor = req["name_of_cor"]
        
        mongo.db.stuPersonalInfo.insert_one({"Student Name": name, "Matric Number": matric_no, "Faculty/Department": faculty, "Course of Study": course_of_study, "Year of Study": year_of_study, "Permanent Home Address": perm_address, "Sex": sex, "Name of Industry-based Supervisor": name_of_sup, "Name of University-based Cordinator": name_of_cor})
        
        flash("Record Added Successfully!", "success")
        return redirect(url_for("add_student_info"))
        
    return render_template("/public/add_student_info.html")

# Route to get company details
@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies = mongo.db.comDetails.find()
    result = []
    for company in companies:
        result.append({
            "student_name": company["Student Name"],
            "name": company["Name of Establishment"],
            "location": company["Location"]
        })
    return jsonify(result)

#Route to add new company details
@app.route("/add-com-details", methods=['GET', 'POST'])
@login_required
def add_com_details():
    if request.method=='POST':
        req = request.form
        
        student_name = req["name_of_stu"]
        name_of_est = req["name_of_est"]
        location = req["location"]
        job = req["job"]
        no_of_emp = req["no_of_emp"]
        telephone = req["telephone"]
        
        mongo.db.comDetails.insert_one({"Student Name": student_name, "Name of Establishment": name_of_est, "Location": location, "Job Undertaken": job, "Number of Employee": no_of_emp, "Telephone": telephone})
        
        flash("Record Added Successfully!", "success")
        return redirect(url_for("add_com_details"))
        
    return render_template("/public/add_company_details.html")

@app.route("/stu-act-report")
@login_required
def stu_act_report():
    return render_template("public/student_act_report.html")

# Route to add weekly activity logging
@app.route("/weekly-activity-logging", methods=['GET', 'POST'])
@login_required
def weekly_activity_logging():
    if request.method=='POST':
        req = request.form
        
        name = req["name"]
        day = req["day"]
        date = req["date"]
        activity = req["activity"]
        
        mongo.db.weeklyActivityLogging.insert_one({"Student Name": name, "Day": day, "Date": date, "Activity": activity})
        
        flash("Record Added Successfully!", "success")
        return redirect(url_for("weekly_activity_logging"))
        
    return render_template("/public/weekly_activity_logging.html")

@app.route("/weekly-activity-summary", methods=['GET', 'POST'])
@login_required
def weekly_activity_summary():
    if request.method=='POST':
        req = request.form
        
        job = req["job"]
        dept = req["dept"]
        comment = req["comment"]
        name = req["name"]
        weekend_date = req["weekend_date"]
        sign = req["sign"]
        
        mongo.db.weeklyActivitySummary.insert_one({"Job of the Week": job, "Department Attached": dept, "Student Comment": comment, "Name of Industry-based Supervisor": name, "Date": weekend_date, "Signature": sign})
        
        flash("Record Added Successfully!", "success")
        return redirect(url_for("weekly_activity_summary"))
        
    return render_template("/public/weekly_activity_summary.html")

@app.route("/all-industries")
@login_required
def all_industries():
    return render_template("public/all_industries.html")

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
# @login_required
def sign_up():
    if request.method=='POST':
        req = request.form
        
        username = str(req["username"])
        usertype = str(req["usertype"])
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
        
        mongo.db.signup.insert_one({"username": username, username:username, "usertype": usertype, "email": email, email:email, "password": password, "activationStatus":"0", "registeredDate": nigerian_time()})
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
            flash("Account not activated! Contact Admin for account activation!!", "danger")
            return render_template("public/index.html")
        
        elif not pswd == checkuser["password"]:
            flash("Username/Password Incorrect!", "danger")
            return render_template("public/index.html")
                  
        else:
            del checkuser["password"]
            session["user"] = checkuser
            session["login"]=True
            if checkuser["usertype"] == "Student":
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for('students_dashboard'))

            elif checkuser["usertype"] == "Supervisor":
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for('supervisor_dashboard'))
            
            else:
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for('admin_dashboard'))
    
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