from app import app, mongo

from flask import render_template, request, url_for, redirect, flash, session

import os, re

from functools import wraps

# from flask_login import current_user

app.config["SECRET_KEY"] = "b'n\x1d\xb1\x8a\xc0Jg\x1d\x08|!F3\x04P\xbf'"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, Please login", 'danger')
            return redirect(url_for("index"))
    return wrap

@app.route("/admin")
@login_required
def admin():
    return render_template("admin/login.html")

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    
    users = mongo.db.sign_up.find({}, {"_id": 0, "user_type": 1, "first_name": 1, "middle_name": 1, "last_name": 1, "matric_number": 1, "email": 1, "activation_status": 1, "signUp_date": 1})
    
    return render_template("admin/admin_dashboard.html", users=users)

@app.route("/admin/admin-profile")
def admin_profile():
    return render_template("admin/admin_profile.html")

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == 'POST':
        req = request.form
        
        name = req["name"]
        mat_number = req["mat_no"]
        email = req["email"]
        reg_date = req["reg_date"]
        address = req["home_addr"]
        marital_status = req["marital_status"]
        level = req["level"]
        gender = req["gender"]
        phone_number = req["phone_number"]
        dob = req["dob"]
        next_of_kin = req["next_of_kin"]
        state = req["state"]
        city = req["city"]
        image = req["image"]
        
        mongo.db.students.insert_one({"full_name": name, "mat_number": mat_number, "email": email, "reg_date": reg_date, "home_address": address, "marital_status": marital_status, "level": level, "gender": gender, "phone_number": phone_number, "date_of_birth": dob, "next_of_kin": next_of_kin, "state": state, "city": city, "image": image})
        
        return redirect(url_for("admin_dashboard"))
                
    return render_template("admin/add_student.html")

@app.route("/add-lecturer", methods=["GET", "POST"])
def add_lecturer():
    if request.method == 'POST':
        req = request.form
        
        staff_no = req["staff_no"]
        title = req["title"]
        f_name = req["f_name"]
        m_name = req["m_name"]
        l_name = req["l_name"]
        email = req["email"]
        position = req["position"]
        dob = req["birthday"]
        state = req["state"]
        res_addr = req["res_addr"]
        gender = req["gender"]
        phone_no = req["phone_no"]
        qual = req["qual"]
        image = req["image"]
        
        mongo.db.staff.insert_one({"staff_number": staff_no, "title": title, "first_name": f_name, "middle_name": m_name, "last_name": l_name, "email": email, "position": postition, "date_of_birth": dob, "state": state, "res_addr": res_addr, "gender": gender, "phone_number": phone_no, "qualification": qual, "image": image})
        
        return redirect(url_for("admin_dashboardd"))
        
    return render_template("admin/add_lecturer.html")

@app.route("/add-course", methods=["GET", "POST"])
def add_course():
    if request.method == 'POST':
        req = request.form
        
        c_title = req["c_title"]
        c_code = req["c_code"]
        c_unit = req["c_unit"]
        level = req["level"]
        lec_name = req["lec_name"]
        semester = req["semester"]
        
        mongo.db.courses.insert_one({"course_title": c_title, "course_code": c_code, "course_unit": c_unit, "level": level, "lec_name": lec_name, "semester": semester})
        
        return redirect(url_for("admin_dashboard"))
        
    return render_template("admin/add_course.html")

@app.route("/edit-student")
def edit_student():
    return render_template("admin/edit_student.html")

@app.route("/edit-course")
def edit_course():
    return render_template("admin/edit_course.html")

@app.route("/edit-lecturer")
def edit_lecturer():
    return render_template("admin/edit_lecturer.html")

@app.route("/all-added-students")
def all_added_students():
    return render_template("admin/all_added_students.html")

@app.route("/all-added-courses")
def all_added_courses():
    return render_template("admin/all_added_courses.html")

@app.route("/all-added-staff")
def all_added_staff():
    return render_template("admin/all_added_staff.html")

@app.route("/all-courses")
def all_courses():
    return render_template("admin/all_courses.html")

@app.route("/all-lecturer-view")
def all_lecturer_view():
    return render_template("admin/all_lecturer_view.html")

@app.route("/all-students-view")
def all_students_view():
    return render_template("admin/all_students_view.html")