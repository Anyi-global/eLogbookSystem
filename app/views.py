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

app.config["UPLOAD_FOLDER"] = "/Users/ANYIGLOBAL/Desktop/MyProject/app/static/uploads"
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

# @app.route("/students/<full_name>")
# def students(full_name):
    
#     users = mongo.db.students.find_one({"full_name": full_name})
    
#     assignments = mongo.db.allAddedAssignments.find({}, {"_id": 0})
    
#     return render_template("public/students_portal.html", user=users)
    
#     return render_template("public/index.html")
    
#     if users["full_name"] in session:
#         user = session["FULL_NAME"]  
#         return render_template("public/students_portal.html", user=user)
    
#     else:
#         flash("User not found in session!", "danger")
#         return render_template("public/grade_students.html")
    
# @app.route("/staff/<middle_name>")
# def staff(middle_name):
#     return render_template("public/lecturer_portal.html")
    
#     user = mongo.db.sign_up.find_one({"middle_name": middle_name})
    
#     return render_template("public/lecturer_portal.html", user=user)
    

@app.route("/staff/dashboard")
@login_required
def staff_dashboard():
    return render_template("public/lecturer_portal.html")

@app.route("/students/dashboard")
@login_required
def students_dashboard():
    return render_template("public/students_portal.html")

@app.route("/add-assignment", methods=['GET', 'POST'])
@login_required
def add_assignment():
    if request.method=='POST':
        req = request.form
        
        course_code = req['course_code']
        assignments = req['asgt']
        submission_date = req['sub_date']
        
        mongo.db.given_assignments.insert_one({"course_code": course_code, "assignments": assignments, "submission_date": submission_date, "datetime_posted": nigerian_time()})
        
        flash("Assignment Added Successfully!", 'success')
        return render_template('public/add_assignment.html')
        
    return render_template("public/add_assignment.html")

@app.route("/all-submitted-assignment-answers")
@login_required
def submitted_assignments():
    return render_template("public/all_submitted_assignment_answers.html")

@app.route("/assignment-answer-submission")
@login_required
def assignment_submission():
    return render_template("public/assignment_answer_submission.html")

@app.route("/all-uploaded-course-forms")
@login_required
def form_uploads():
    return render_template("public/course_form_uploads.html")

@app.route("/downloaded-course-forms")
@login_required
def downloaded_forms():
    
    return render_template("public/downloaded_course_forms.html")

@app.route("/grade-students", methods=['GET', 'POST'])
@login_required
def grade_students():
    if request.method == 'POST':
        req = request.form
        
        mat_no = req['mat_no']
        course_code = req['course_code']
        score = req['score']
        remark = req['remark']
        
        mongo.db.grades.insert_one({"matric_number": mat_no, "course_code": course_code, "score": score, "datetime_posted": nigerian_time()})
        
        flash("Student Grade Added Successfully!", 'success')
        return render_template("public/grade_students.html")
    
    return render_template("public/grade_students.html")

@app.route("/lecturers-profile")
@login_required
def lecturers_profile():
    return render_template("public/lecturers_profile.html")
    # if request.method=='POST':
    #     req = request.form
        
    #     full_name = req["fullName"]
    #     about = req["about"]
    #     company = req["company"]
    #     job = req["job"]
    #     country = req["country"]
    #     address = req["address"]
    #     phone = req["phone"]
    #     email = req["email"]
    #     twitter = req["twitter"]
    #     facebook = req["facebook"]
    #     instagram = req["instagram"]
    #     linkedin = req["linkedin"]    
    
    # checkuser = mongo.db.sign_up.find_one({"matric_number"})
    
    # if session.get("MATRIC_NUMBER", None) is not none:
    #     matric_number = session.get("MATRIC_NUMBER")
    #     user = checkuser["matric_number"]
    #     return render_template("public/lecturers_profile.html", user=user)
    # else:
    #     flash("Matric Number is not found in session", 'danger')
    #     return redirect(url_for("login"))
    

@app.route("/student-profile")
@login_required
def student_profile():
    return render_template("public/student_profile.html")

@app.route("/all-given-assignments")
@login_required
def all_given_assignments():
    return render_template("public/view_all_given_assignments.html")

@app.route("/view-assignment-score")
@login_required
def view_assignment_score():
    return render_template("public/view_assignment_score.html")

# Allowed Image Extension Names to Upload
# def allowed_image(filename):
#     if not "." in filename:
#         return False
#     ext = filename.rsplit(".", 1)[1]
#     if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
#         return True
#     else:
#         return False

# class CourseForm(db.Document):
#     mat_no = db.StringField()
#     level = db.StringField()
#     course_form = db.StringField()

# Allowed files to be uploaded
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in app.config["ALLOWED_EXTENSIONS"]

@app.route('/upload-course-form', methods=["GET", "POST"])
def upload_course_form():
    if request.method=='POST':
        if 'file' not in request.files:
            flash("No file part!", 'warning')
            return render_template("public/upload_course_form.html")
        file = request.files['file']
        if file.filename=='':
            flash("No selected file, please select a file", 'warning')
            return render_template("public/upload_course_form.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)   
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("File uploaded successfully", 'success')
            return render_template("public/upload_course_form.html")
    return render_template("public/upload_course_form.html")

# @app.route("/upload-course-form", methods=['GET', 'POST'])
# def upload_course_form():
#     if request.method == 'POST':  
#         # if request.files:
        
#         mat_no = str(request.form['mat_no']).upper()
#         level = str(request.form['level'])   
#         course_form = request.form["course_form"]   
            
            # if course_form.filename == "":
            #     flash("Image must have a name!", 'danger')
            #     return render_template("public/upload_course_form.html")
            
            # elif not allowed_image(course_form.filename):
            #     flash("That Image Extension is not allowed!", 'danger')
            #     return render_template("public/upload_course_form.html")
                
            # else:
                # filename = secure_filename(course_form.filename)
    #     mongo.db.Course_forms.insert_one({"matric_number": mat_no, "level": level, "course_form": course_form,  "datetime_posted": nigerian_time()})
    #     flash("Course Form Submitted Successfully!", 'success')
    #     return render_template("public/upload_course_form.html")
    
    # return render_template("public/upload_course_form.html")

# app.config["SECRET_KEY"] = 'qOvd3CvKNglEYbhM1yFK0Q'

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method=='POST':
        req = request.form
        
        user_type = str(req["user_type"]).upper()
        f_name = str(req["f_name"]).upper()
        m_name = str(req["m_name"]).upper()
        l_name = str(req["l_name"]).upper()
        mat_no = str(req["mat_no"]).upper()
        email = str(req["email"]).lower()
        password = req["pswd"]
        con_password = req["con_pswd"]
        
        matric_number = mat_no.split('/')
        
        if password != con_password:
            flash("Password Confirmation Mismatched, Please Confirm Your Password!", "danger")
            return render_template("public/register.html")
        elif matric_number[2] != 'CSI':
            flash("Sorry, Wrong matric number format!", "danger")
            return render_template("public/register.html")
        elif matric_number[0] != 'FUO':
            flash("Sorry, Wrong matric number format!", "danger")
            return render_template("public/register.html")
        # checkuser = mongo.db.sign_up.find_one({"matric_number":mat_no}, {"_id":0})
        checkuser = mongo.db.sign_up.find_one({mat_no:{"$exists":True}}, {"_id":0})
        if checkuser:
            flash("Sorry, User already registered!", "danger")
            return render_template("public/register.html")
        # checkemail = mongo.db.sign_up.find_one({"email":email}, {"_id":0})
        checkemail = mongo.db.sign_up.find_one({email:{"$exists":True}}, {"_id":0})
        if checkemail:
            flash("Sorry, User with email address already exists!", "danger")
            return render_template("public/register.html")
        
        mongo.db.sign_up.insert_one({"user_type": user_type, "first_name": f_name, "middle_name": m_name, "last_name": l_name, "matric_number": mat_no, mat_no:mat_no, "email": email, email:email, "password": password, "activation_status":"0", "signUp_date": nigerian_time()})
        flash("Account Created Successfully!", "success")
        return redirect(url_for("index"))
    else:
        return render_template("public/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=='POST':
        req = request.form
        
        mat_no = str(req["mat_no"]).upper()
        pswd = req["pswd"]
        
        # checkuser = mongo.db.sign_up.find_one({"matric_number": mat_no})
        checkuser = mongo.db.sign_up.find_one({mat_no:{"$exists":True}}, {"_id":0})
        
        # x = re.search(pattern, string)
        
        if not checkuser:
            flash("Matric No./Password Incorrect!", "danger")
            return render_template("public/index.html")
        
        elif checkuser["activation_status"] != "1":
            flash("Account not activated. Contact Admin!", "danger")
            return render_template("public/index.html")
        
        elif not pswd == checkuser["password"]:
            flash("Matric No./Password Incorrect!", "danger")
            return render_template("public/index.html")
                  
        else:
            del checkuser["password"]
            session["user"] = checkuser
            session["login"]=True
            if checkuser["user_type"] == "STUDENT":
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for("students_dashboard"))
            
            elif checkuser["user_type"] == "STAFF":
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for("staff_dashboard"))
            
            elif checkuser["user_type"] == "ADMIN":
                flash("Logged in Successfully! Welcome to your Dashboard!!", "success")
                return redirect(url_for("admin_dashboard"))
    
    return render_template("public/index.html")

        
@app.route("/edit_profile", methods=["POST"])
@login_required
def edit_profile():
    req = request.form
    
    mat_no = str(req["mat_no"]).upper()
    new_email = str(req["email"]).lower()
    
    # checkuser = mongo.db.sign_up.find_one({"matric_number":mat_no}, {"_id":0})
    checkuser = mongo.db.sign_up.find_one({mat_no:{"$exists":True}}, {"_id":0})
    if not checkuser:
        flash("Sorry, User not registered!", "danger")
        return render_template("public/student_profile.html")
    # checkemail = mongo.db.sign_up.find_one({"email":email}, {"_id":0})
    checkemail = mongo.db.sign_up.find_one({new_email:{"$exists":True}}, {"_id":0})
    if checkemail:
        flash("Sorry, User with email address already exists!", "danger")
        return render_template("public/student_profile.html")
    
    old_email = checkuser["email"]
    # mongo.db.sign_up.update_one({mat_no:{"$exists":True}}, {"$unset": {"email": old_email,:new_email}})
    mongo.db.sign_up.update_one({mat_no:{"$exists":True}}, {"$set": {"email": new_email, new_email:new_email}})
    flash("Profile Updated Successfully!", "success")
    return redirect(url_for("student-profile"))