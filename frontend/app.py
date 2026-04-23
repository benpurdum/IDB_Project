from flask import Flask, render_template, request, redirect, url_for, session
import config
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = config.dbserver

app = Flask(__name__)
app.debug = True

app.secret_key = 'Epic Ben and Zoe Website'
departments = ["Do Not Update", "Music", "History", "Biology", "Comp. Sci.", "Elec. Eng.", "Finance", "Physics"]

@app.route('/')
def index():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    account = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()

        sql = "SELECT * FROM accounts WHERE username = %s"
        cursor.execute(sql, [username])
        account = cursor.fetchone()
        cursor.close()
    

        #check if user + password is correct
        if account and check_password_hash(account[2], password):
            print("seccuess")
            session['loggedin'] = True
            session['id'] = account[0] 
            session['username'] = account[1]
            session['password'] = account[2]
            session['permission'] = account[3]
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'   

    return render_template('index.html', msg=msg)

@app.route('/home')
def home():
    if 'loggedin' in session:
        #print(session['permission'])
        return render_template('home.html', username=session['username'], permission=session['permission'])
    return redirect(url_for('login'))

# Logout 
@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('permission', None)
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET','POST'])
def settings():
    cursor = db.cursor()
    departments = ["Do Not Update", "Music", "History", "Biology", "Comp. Sci.", "Elec. Eng.", "Finance", "Physics"]
    
    if request.method == 'POST':
        username = request.form['username']
        badpassword = request.form['password']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        secondname = request.form['secondname']
        department = request.form['dept']
        print(firstname)
        print(middlename)
        print(lastname)
        print(secondname)

        if username:
            sql = "call updateUsername(%s,%s)"
            cursor.execute(sql, (session['id'], username))
            db.commit()
            session.pop('username', None)
            session['username'] = username
        if badpassword:
            sql = "call changePassword(%s,%s)"
            password = generate_password_hash(badpassword)
            cursor.execute(sql, (session['id'], password))
        if department != "Do Not Update":
            if session['permission'] == "Instructor":
                sql = "call updateInstructorDept(%s,%s)"
                cursor.execute(sql, (session['id'], department))
                db.commit()
            elif session['permission'] == "Student":
                sql = "call updateStudentDept(%s,%s)"
                cursor.execute(sql, (session['id'], department))
                db.commit()
        if firstname or middlename or lastname or secondname:
            if session['permission'] == "Instructor":
                sql = "call updateInstructorName(%s,%s,%s,%s,%s)"
                cursor.execute(sql, (session['id'], firstname, middlename, lastname, secondname))
                db.commit()
            elif session['permission'] == "Student":
                sql = "call updateStudentName(%s,%s,%s,%s,%s)"
                cursor.execute(sql, (session['id'], firstname, middlename, lastname, secondname))
                db.commit()

    if session['permission'] == "Student":
        sql = "call findStudent(%s)"
        cursor.execute(sql, session['id'])
        account = cursor.fetchone()
        data = [account[0], account[4], account[5], account[6], account[7], account[2]]
    elif session['permission'] == "Instructor":
        sql = "call findInstructor(%s)"
        cursor.execute(sql, session['id'])
        account = cursor.fetchone()
        data = [account[0], account[5], account[6], account[7], account[8], account[2], account[3]]
    else:
        data = [session['id'], 'admin', 'admin', 'admin', 'admin', 'admin']

    cursor.close()
    return render_template('settings.html', data=data, departments=departments)

#admin stuff
@app.route('/addstudent', methods=['GET','POST'])
@app.route('/readstudent', methods=['GET','POST'])
def readStudent():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllStudents()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Student', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findStudent(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Student', data=data)

@app.route('/updatestudent', methods=['GET','POST'])
@app.route('/deletestudent', methods=['GET','POST'])
@app.route('/addinstructor', methods=['GET','POST'])
@app.route('/readinstructor', methods=['GET','POST'])
def readInstructor():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllInstructors()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Instructor', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findInstructor(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Instructor', data=data)
    
@app.route('/updateinstructor', methods=['GET','POST'])
@app.route('/deleteinstructor', methods=['GET','POST'])
@app.route('/adddept', methods=['GET','POST'])
@app.route('/readdept', methods=['GET','POST'])
def readDept():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Dept', data=data)
    if request.method == 'POST':
        id = request.form['name']
        cursor = db.cursor()
        sql = "call findDept(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Dept', data=data)

@app.route('/updatedept', methods=['GET','POST'])
@app.route('/deletedept', methods=['GET','POST'])
@app.route('/addclassroom', methods=['GET','POST'])
@app.route('/readclassroom', methods=['GET','POST'])
def readClassroom():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllClassrooms()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Classroom', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findClassroom(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Classroom', data=data)

@app.route('/updateclassroom', methods=['GET','POST'])
@app.route('/deleteclassroom', methods=['GET','POST'])
@app.route('/addcourse', methods=['GET','POST'])
@app.route('/readcourse', methods=['GET','POST'])
def readCourse():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllCourses()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Course', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findCourse(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Course', data=data)

@app.route('/updatecourse', methods=['GET','POST'])
@app.route('/deletecourse', methods=['GET','POST'])
@app.route('/addsection', methods=['GET','POST'])
@app.route('/readsection', methods=['GET','POST'])
def readSection():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllSections()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Section', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findSectionsOfClass(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Section', data=data)

@app.route('/updatesection', methods=['GET','POST'])
@app.route('/deletesection', methods=['GET','POST'])
@app.route('/addtimeslot', methods=['GET','POST'])
@app.route('/readtimeslot', methods=['GET','POST'])
def readTimeSlot():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllTimeslots()"
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('show.html', show='Time Slot', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findTimeslot(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Time Slot', data=data)

@app.route('/updatetimeslot', methods=['GET','POST'])
@app.route('/deletetimeslot', methods=['GET','POST'])
@app.route('/assignteacher', methods=['GET','POST'])
@app.route('/modifyteacher', methods=['GET','POST'])
@app.route('/removeteacher', methods=['GET','POST'])

#instructor stuff
@app.route('/submitgrades')
@app.route('/changegrades')
@app.route('/addstudentadvisor')
@app.route('/removestudentadvisor')
@app.route('/checkroster')
@app.route('/checksemesterroster')
@app.route('/removestudentfromsection')
@app.route('/addprereq')
@app.route('/modifyprereq')

#student stuff
@app.route('/registerclass')
@app.route('/sectioninfo')
@app.route('/advisorinfo')
def addstudent():
    return 0