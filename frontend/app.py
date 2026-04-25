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
    sql = "call getAllDepts()"
    cursor.execute(sql)
    data = cursor.fetchall()
    depts = []
    depts.append("Do Not Update")
    for i in data:
        depts.append(i[0])
    
    if request.method == 'POST':
        username = request.form['username']
        badpassword = request.form['password']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        secondname = request.form['secondname']
        department = request.form['dept']

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
    return render_template('settings.html', data=data, departments=depts)

#admin stuff
@app.route('/addstudent', methods=['GET','POST'])
def addstudent():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('add.html', show='Student', depts=depts)
    if request.method == 'POST':
        id = request.form['id']
        nid = request.form['nid']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        secondname = request.form['secondname']
        department = request.form['dept']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        cursor = db.cursor()
        sql = "call createStudent(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (id,nid,firstname,middlename,lastname,secondname,department,username,password))
        db.commit()

        sql = "call findStudent(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Student', data=data)

@app.route('/readstudent', methods=['GET','POST'])
def readStudent():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllStudents()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Student', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findStudent(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Student', data=data)

@app.route('/updatestudent', methods=['GET','POST'])
def updateStudent():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        depts.append("Do Not Update")
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('update.html', show='Student', depts=depts)
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        secondname = request.form['secondname']
        department = request.form['dept']
        cursor = db.cursor()

        if username:
            sql = "call updateUsername(%s,%s)"
            cursor.execute(sql, (id, username))
            db.commit()
            session.pop('username', None)
            session['username'] = username
        if password:
            sql = "call changePassword(%s,%s)"
            cursor.execute(sql, (id, generate_password_hash(password)))
        if department != "Do Not Update":
            sql = "call updateStudentDept(%s,%s)"
            cursor.execute(sql, (id, department))
            db.commit()
        if firstname or middlename or lastname or secondname:
            sql = "call updateStudentName(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id, firstname, middlename, lastname, secondname))
            db.commit()
        
        sql = "call findStudent(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Student', data=data)

@app.route('/deletestudent', methods=['GET','POST'])
def deleteStudent():
    if request.method == 'GET':
        return render_template('delete.html', show='Student', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "select * from takes where ID = %s"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a student that is registered to classes."
            return render_template('delete.html', show='Student', msg=msg)

        sql = "call deleteStudent(%s)"
        cursor.execute(sql, (id))
        db.commit()
        cursor.close()
        return redirect('/readstudent')

@app.route('/addinstructor', methods=['GET','POST'])
def addInstructor():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('add.html', show='Instructor', depts=depts)
    if request.method == 'POST':
        id = request.form['id']
        nid = request.form['nid']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        secondname = request.form['secondname']
        department = request.form['dept']
        salary = request.form['salary']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        cursor = db.cursor()
        sql = "call createInstructor(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (id,nid,firstname,middlename,lastname,secondname,department,salary,username,password))
        db.commit()

        sql = "call findInstructor(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Instructor', data=data)

@app.route('/readinstructor', methods=['GET','POST'])
def readInstructor():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllInstructors()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Instructor', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findInstructor(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Instructor', data=data)
    
@app.route('/updateinstructor', methods=['GET','POST'])
def updateInstructor():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        depts.append("Do Not Update")
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('update.html', show='Instructor', depts=depts)
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        secondname = request.form['secondname']
        department = request.form['dept']
        salary = request.form['salary']
        cursor = db.cursor()

        if username:
            sql = "call updateUsername(%s,%s)"
            cursor.execute(sql, (id, username))
            db.commit()
            session.pop('username', None)
            session['username'] = username
        if password:
            sql = "call changePassword(%s,%s)"
            cursor.execute(sql, (id, generate_password_hash(password)))
        if department != "Do Not Update":
            sql = "call updateInstructorDept(%s,%s)"
            cursor.execute(sql, (id, department))
            db.commit()
        if firstname or middlename or lastname or secondname:
            sql = "call updateInstructorName(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id, firstname, middlename, lastname, secondname))
            db.commit()
        if salary:
            sql = "call updateInstructorSalary(%s,%s)"
            cursor.execute(sql, (id, salary))
            db.commit()
        
        sql = "call findInstructor(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Instructor', data=data)

@app.route('/deleteinstructor', methods=['GET','POST'])
def deleteInstructor():
    if request.method == 'GET':
        return render_template('delete.html', show='Instructor', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()

        sql = "select * from teaches where ID = %s"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete an instructor that is teaching classes."
            return render_template('delete.html', show='Instructor', msg=msg)

        sql = "call deleteInstructor(%s)"
        cursor.execute(sql, (id))
        db.commit()
        cursor.close()
        return redirect('/readinstructor')

@app.route('/adddept', methods=['GET','POST'])
def addDept():
    if request.method == 'GET':
        return render_template('add.html', show='Dept')
    if request.method == 'POST':
        name = request.form['name']
        building = request.form['building']
        budget = request.form['budget']
        cursor = db.cursor()
        sql = "call createDept(%s,%s,%s)"
        cursor.execute(sql, (name,building,budget))
        db.commit()

        sql = "call findDept(%s)"
        cursor.execute(sql, name)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Dept', data=data)

@app.route('/readdept', methods=['GET','POST'])
def readDept():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Dept', data=data)
    if request.method == 'POST':
        id = request.form['name']
        cursor = db.cursor()
        sql = "call findDept(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Dept', data=data)

@app.route('/updatedept', methods=['GET','POST'])
def updateDept():
    if request.method == 'GET':
        return render_template('update.html', show='Dept')
    if request.method == 'POST':
        name = request.form['name']
        building = request.form['building']
        budget = request.form['budget']
        cursor = db.cursor()
        sql = "call updateDept(%s,%s,%s)"
        cursor.execute(sql, (name,building,budget))
        db.commit()

        sql = "call findDept(%s)"
        cursor.execute(sql, name)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Dept', data=data)

@app.route('/deletedept', methods=['GET','POST'])
def deleteDept():
    if request.method == 'GET':
        return render_template('delete.html', show='Dept', msg='')
    if request.method == 'POST':
        id = request.form['name']
        cursor = db.cursor()

        sql = "select * from instructor, student where instructor.dept_name = %s or student.dept_name = %s"
        cursor.execute(sql, (id, id))
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a department with registered members."
            return render_template('delete.html', show='Dept', msg=msg)

        sql = "call deleteDept(%s)"
        cursor.execute(sql, (id))
        db.commit()
        cursor.close()
        return redirect('/readdept')

@app.route('/addclassroom', methods=['GET','POST'])
def addClassroom():
    if request.method == 'GET':
        return render_template('add.html', show='Classroom')
    if request.method == 'POST':
        id = request.form['id']
        building = request.form['building']
        roomnumber = request.form['roomnumber']
        capacity = request.form['capacity']
        cursor = db.cursor()
        sql = "call createClassroom(%s,%s,%s,%s)"
        cursor.execute(sql, (id,building,roomnumber,capacity))
        db.commit()

        sql = "call findClassroom(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Classroom', data=data)

@app.route('/readclassroom', methods=['GET','POST'])
def readClassroom():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllClassrooms()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Classroom', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findClassroom(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        return render_template('show.html', show='Classroom', data=data)

@app.route('/updateclassroom', methods=['GET','POST'])
def updateClassroom():
    if request.method == 'GET':
        return render_template('update.html', show='Classroom')
    if request.method == 'POST':
        id = request.form['id']
        building = request.form['building']
        roomnumber = request.form['roomnumber']
        capacity = request.form['capacity']
        if capacity == '':
            capacity = -1
        cursor = db.cursor()
        sql = "call updateClassroom(%s,%s,%s,%s)"
        cursor.execute(sql, (id,building,roomnumber,capacity))
        db.commit()

        sql = "call findClassroom(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Classroom', data=data)

@app.route('/deleteclassroom', methods=['GET','POST'])
def deleteClassroom():
    if request.method == 'GET':
        return render_template('delete.html', show='Classroom', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call deleteClassroom(%s)"

        sql = "select * from section where room_id = %s"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a room that is in use."
            return render_template('delete.html', show='Classroom', msg=msg)

        cursor.execute(sql, (id))
        db.commit()
        cursor.close()
        return redirect('/readclassroom')

@app.route('/addcourse', methods=['GET','POST'])
def addCourse():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('add.html', show='Course', depts=depts)
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        dept = request.form['dept']
        credits = request.form['credits']
        cursor = db.cursor()
        sql = "call createCourse(%s,%s,%s,%s)"
        cursor.execute(sql, (id,title,dept,credits))
        db.commit()

        sql = "call findCourse(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Course', data=data)

@app.route('/readcourse', methods=['GET','POST'])
def readCourse():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllCourses()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Course', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findCourse(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Course', data=data)

@app.route('/updatecourse', methods=['GET','POST'])
def updateCourse():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        depts.append("Do Not Update")
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('update.html', show='Course', depts=depts)
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        dept = request.form['dept']
        if dept == "Do Not Update":
            dept = ''
        credits = request.form['credits']
        if credits == '':
            credits = -1
        cursor = db.cursor()
        sql = "call updateCourse(%s,%s,%s,%s)"
        cursor.execute(sql, (id,title,dept,credits))
        db.commit()

        sql = "call findCourse(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Course', data=data)

@app.route('/deletecourse', methods=['GET','POST'])
def deleteCourse():
    if request.method == 'GET':
        return render_template('delete.html', show='Course', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call deleteCourse(%s)"

        sql = "select * from takes, teaches where takes.course_id = %s or teaches.course_id = %s"
        cursor.execute(sql, (id, id))
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a course being taught."
            return render_template('delete.html', show='Course', msg=msg)

        cursor.execute(sql, (id))
        db.commit()
        cursor.close()
        return redirect('/readcourse')

@app.route('/addsection', methods=['GET','POST'])
def addSection():
    if request.method == 'GET':
        return render_template('add.html', show='Section')
    if request.method == 'POST':
        cid = request.form['cid']
        sid = request.form['sid']
        semester = request.form['semester']
        year = request.form['year']
        building = request.form['building']
        rid = request.form['rid']
        tid = request.form['tid']
        cursor = db.cursor()
        sql = "call createSection(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (cid, sid, semester, year, building, rid, tid))
        db.commit()

        sql = "call findSectionsOfClass(%s)"
        cursor.execute(sql, cid)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Section', data=data)

@app.route('/readsection', methods=['GET','POST'])
def readSection():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllSections()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Section', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findSectionsOfClass(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Section', data=data)

@app.route('/updatesection', methods=['GET','POST'])
def updateSection():
    if request.method == 'GET':
        return render_template('update.html', show='Section')
    if request.method == 'POST':
        cid = request.form['cid']
        sid = request.form['sid']
        building = request.form['building']
        rid = request.form['rid']
        cursor = db.cursor()
        if building:
            sql = "call updateSectionBuilding(%s,%s,%s)"
            cursor.execute(sql, (cid,sid,building))
            db.commit()
        if rid:
            sql = "call updateSectionRoomID(%s,%s,%s)"
            cursor.execute(sql, (cid,sid,rid))
            db.commit()

        sql = "call findSectionsOfCLass(%s)"
        cursor.execute(sql, (cid))
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='Classroom', data=data)

@app.route('/deletesection', methods=['GET','POST'])
def deleteSection():
    if request.method == 'GET':
        return render_template('delete.html', show='Section', msg='')
    if request.method == 'POST':
        cid = request.form['cid']
        sid = request.form['sid']
        cursor = db.cursor()

        sql = "select * from takes where takes.course_id = %s and takes.sec_id = %s"
        cursor.execute(sql, (cid, sid))
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a section being taught."
            return render_template('delete.html', show='Section', msg=msg)
        sql = "select * from teaches where teaches.course_id = %s and teaches.sec_id = %s"
        cursor.execute(sql, (cid, sid))
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a section being taught."
            return render_template('delete.html', show='Section', msg=msg)

        sql = "call deleteSection(%s,%s)"
        cursor.execute(sql, (sid,cid))
        db.commit()
        cursor.close()
        return redirect('/readsection')

@app.route('/addtimeslot', methods=['GET','POST'])
def addTimeSlot():
    if request.method == 'GET':
        return render_template('add.html', show='TimeSlot')
    if request.method == 'POST':
        id = request.form['id']
        day = request.form['day']
        starthr = request.form['starthr']
        startmin = request.form['startmin']
        endhr = request.form['endhr']
        endmin = request.form['endmin']
        cursor = db.cursor()
        sql = "call createTimeSlot(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (id, day, starthr, startmin, endhr, endmin))
        db.commit()

        sql = "call findTimeSlot(%s)"
        cursor.execute(sql, (id))
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='TimeSlot', data=data)

@app.route('/readtimeslot', methods=['GET','POST'])
def readTimeSlot():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllTimeslots()"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='TimeSlot', data=data)
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call findTimeslot(%s)"
        cursor.execute(sql, id)
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='TimeSlot', data=data)

@app.route('/updatetimeslot', methods=['GET','POST'])
def updateTimeSlot():
    if request.method == 'GET':
        return render_template('update.html', show='TimeSlot')
    if request.method == 'POST':
        id = request.form['id']
        day = request.form['day']
        starthr = request.form['starthr']
        startmin = request.form['startmin']
        endhr = request.form['endhr']
        endmin = request.form['endmin']

        if starthr == '':
            starthr = -1
        if startmin == '':
            startmin = -1
        if endhr == '':
            endhr = -1
        if endmin == '':
            endmin = -1

        cursor = db.cursor()
        sql = "call updateTimeSlot(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (id, day, starthr, startmin, endhr, endmin))
        db.commit()

        sql = "call findTimeSlot(%s)"
        cursor.execute(sql, (id))
        data = cursor.fetchall()
        cursor.close()
        return render_template('show.html', show='TimeSlot', data=data)

@app.route('/deletetimeslot', methods=['GET','POST'])
def deleteTimeSlot():
    if request.method == 'GET':
        return render_template('delete.html', show='TimeSlot', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cursor = db.cursor()
        sql = "call deleteTimeSlot(%s)"

        sql = "select * from section where time_slot_id = %s"
        cursor.execute(sql, (id))
        data = cursor.fetchall()
        if data:
            msg = "Cannot delete a time slot being used."
            return render_template('delete.html', show='Course', msg=msg)

        cursor.execute(sql, (id))
        db.commit()
        cursor.close()
        return redirect('/readtimeslot')

@app.route('/assignteacher', methods=['GET','POST'])
def assignTeacher():
    if request.method == 'GET':
        return render_template('add.html', show='Teacher', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cid = request.form['cid']
        sid = request.form['sid']
        semester = request.form['semester']
        year = int(request.form['year'])
        cursor = db.cursor()

        sql = "call findSectionsOfClass(%s)"
        cursor.execute(sql, cid)
        data = cursor.fetchall()
        querygood = False
        for i in data:
            if i[0] == cid and i[1] == sid and i[2] == semester and i[3] == year:
                querygood = True
        
        if querygood:
            sql = "call assignInstructor(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (id, cid, sid, semester, year))
            db.commit()
            return render_template('add.html', show='Teacher', msg="Success!")
        return render_template('add.html', show='Teacher', msg="Assignment Failed.")

@app.route('/modifyteacher', methods=['GET','POST'])
def modifyTeacher():
    if request.method == 'GET':
        return render_template('update.html', show='Teacher', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cid = request.form['cid']
        sid = request.form['sid']
        cursor = db.cursor()
        sql = "call modifyTeacher(%s,%s,%s)"
        cursor.execute(sql, (id, cid, sid))
        db.commit()
        return render_template('update.html', show='Teacher', msg="Success!")

@app.route('/removeteacher', methods=['GET','POST'])
def removeTeacher():
    if request.method == 'GET':
        return render_template('delete.html', show='Teacher', msg='')
    if request.method == 'POST':
        id = request.form['id']
        cid = request.form['cid']
        sid = request.form['sid']
        cursor = db.cursor()
        sql = "call removeTeacher(%s,%s,%s)"
        cursor.execute(sql, (id, cid, sid))
        db.commit()
        return render_template('delete.html', show='Teacher', msg="Success!")

#EXTRA STUFF I NEED
#average grade of all students by dept
@app.route('/averagegradedept', methods=['GET','POST'])
def averageGradeDept():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('average.html', show='GetDept', depts=depts)
    if request.method == 'POST':
        dept = request.form['dept']
        cursor = db.cursor()
        sql = "select * from student, takes where student.id = takes.id and student.dept_name = %s;"
        cursor.execute(sql, dept)
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return render_template('average.html', show='NoData')
        #f d- d d+ c- c c+ b- b b+ a- a
        #1 2  3 4  5  6 7  8  9 10 11 12
        grades = []
        for i in data:
            match i[8]:
                case 'F':
                    grades.append(1)
                case 'D-':
                    grades.append(2)
                case 'D':
                    grades.append(3)
                case 'D+':
                    grades.append(4)
                case 'C-':
                    grades.append(5)
                case 'C':
                    grades.append(6)
                case 'C+':
                    grades.append(7)
                case 'B-':
                    grades.append(8)
                case 'B':
                    grades.append(9)
                case 'B+':
                    grades.append(10)
                case 'A-':
                    grades.append(11)
                case 'A':
                    grades.append(12)
                case 'A+':
                    grades.append(13)
        sum = 0
        for i in grades:
            sum += i
        avg = int(sum / len(grades))
        match avg:
            case 1:
                grade = 'F'
            case 2:
                grade = 'D-'
            case 3:
                grade = 'D'
            case 4:
                grade = 'D+'
            case 5:
                grade = 'C-'
            case 6:
                grade = 'C'
            case 7:
                grade = 'C+'
            case 8:
                grade = 'B-'
            case 9:
                grade = 'B'
            case 10:
                grade = 'B+'
            case 11:
                grade = 'A-'
            case 12:
                grade = 'A'
            case 13:
                grade = 'A+'
        return render_template('average.html', show='ShowDept', dept=dept, grade=grade)


#average grade of a class by semester range
@app.route('/averagegradeclasssem', methods=['GET','POST'])
def averageGradeClassSem():
    if request.method == 'GET':
        return render_template('average.html', show='GetSem')
    if request.method == 'POST':
        cid = request.form['cid']
        bsem = request.form['bsem']
        byear = request.form['byear']
        esem = request.form['esem']
        eyear = request.form['eyear']

        cursor = db.cursor()
        sql = "select * from takes where takes.course_id=%s and takes.year>=%s and takes.year<=%s;"
        cursor.execute(sql, (cid,byear,eyear))
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return render_template('average.html', show='NoData')

        grades = []
        for i in data:
            match i[5]:
                case 'F':
                    grades.append(1)
                case 'D-':
                    grades.append(2)
                case 'D':
                    grades.append(3)
                case 'D+':
                    grades.append(4)
                case 'C-':
                    grades.append(5)
                case 'C':
                    grades.append(6)
                case 'C+':
                    grades.append(7)
                case 'B-':
                    grades.append(8)
                case 'B':
                    grades.append(9)
                case 'B+':
                    grades.append(10)
                case 'A-':
                    grades.append(11)
                case 'A':
                    grades.append(12)
                case 'A+':
                    grades.append(13)
        sum = 0
        for i in grades:
            sum += i
        avg = int(sum / len(grades))
        match avg:
            case 1:
                grade = 'F'
            case 2:
                grade = 'D-'
            case 3:
                grade = 'D'
            case 4:
                grade = 'D+'
            case 5:
                grade = 'C-'
            case 6:
                grade = 'C'
            case 7:
                grade = 'C+'
            case 8:
                grade = 'B-'
            case 9:
                grade = 'B'
            case 10:
                grade = 'B+'
            case 11:
                grade = 'A-'
            case 12:
                grade = 'A'
            case 13:
                grade = 'A+'
        return render_template('average.html', show='ShowSem', grade=grade, cid=cid, bsem=bsem, byear=byear, esem=esem, eyear=eyear)

#best and worst performing classes (on average grade) by semester
@app.route('/bestworstclasssem', methods=['GET','POST'])
def bestWorstClassSem():
    if request.method == 'GET':
        return render_template('average.html', show="GetBestWorst")
    if request.method == 'POST':
        sem = request.form['sem']
        year = request.form['year']
        cursor = db.cursor()
        sql = "select * from takes where semester=%s and year=%s"
        cursor.execute(sql,(sem,year))
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return render_template('average.html', show='NoData')

        courses = []
        for i in data:
            temp = 0
            match i[5]:
                case 'F':
                    temp = 1
                case 'D-':
                    temp = 2
                case 'D':
                    temp = 3
                case 'D+':
                    temp = 4
                case 'C-':
                    temp = 5
                case 'C':
                    temp = 6
                case 'C+':
                    temp = 7
                case 'B-':
                    temp = 8
                case 'B':
                    temp = 9
                case 'B+':
                    temp = 10
                case 'A-':
                    temp = 11
                case 'A':
                    temp = 12
                case 'A+':
                    temp = 13
            courses.append([i[1],temp])
        
        totals = {}
        counts = {}

        for course, grade in courses:
            if course not in totals:
                totals[course] = 0
                counts[course] = 0
            
            totals[course] += grade
            counts[course] += 1

        averages = {}
        for course in totals:
            averages[course] = totals[course] / counts[course]

        bcid = ""
        wcid = ""
        btemp = 0
        wtemp = 13
        for course, avg in averages.items():
            if avg > btemp:
                btemp = avg
                bcid = course
                print("b",bcid,avg)
            if avg < wtemp:
                wtemp = avg
                wcid = course
                print("w",wcid,avg)

        return render_template('average.html', show='ShowBestWorst', bcid=bcid, wcid=wcid)

#total students by dept
@app.route('/totalstudentsdept', methods=['GET','POST'])
def totalStudentsDept():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('average.html', show='GetStudentDept', depts=depts)
    if request.method == 'POST':
        dept = request.form['dept']
        cursor = db.cursor()
        sql = "select * from student where dept_name=%s"
        cursor.execute(sql, dept)
        data = cursor.fetchall()
        count = len(data)
        cursor.close()
        return render_template('average.html', show='ShowStudentDept', count=count, dept=dept)

#total current students by dept
@app.route('/currentstudentsdept', methods=['GET','POST'])
def currentStudentsDept():
    if request.method == 'GET':
        cursor = db.cursor()
        sql = "call getAllDepts()"
        cursor.execute(sql)
        data = cursor.fetchall()
        depts = []
        for i in data:
            depts.append(i[0])
        cursor.close()
        return render_template('average.html', show='GetCurrentDept', depts=depts)
    if request.method == 'POST':
        dept = request.form['dept']
        cursor = db.cursor()
        sql = "select * from student, takes where student.ID = takes.ID and student.dept_name=%s and takes.semester='Spring' and takes.year=2026"
        cursor.execute(sql, dept)
        data = cursor.fetchall()
        count = len(data)
        cursor.close()
        return render_template('average.html', show='ShowCurrentDept', count=count, dept=dept)

#instructor stuff
@app.route('/submitgrades', methods=['GET','POST'])
def submitGrades():
        cursor = db.cursor()

        input_studentid = request.form.get('student_id')
        input_courseid = request.form.get('course_id')
        input_secid = request.form.get('sec_id')
        input_semester = request.form.get('semester')
        input_year = request.form.get('year')
        input_grade = request.form.get('grade')

    
        cursor.execute('CALL gradeSection(%s, %s, %s, %s, %s, %s)', (input_studentid, input_courseid, input_secid, input_semester, input_year, input_grade))
        db.commit()
        cursor.close()

        return render_template('submitgrades.html')


@app.route('/addstudentadvisor', methods=['GET','POST'])
def addStudentAdvisor():

    if request.method == 'POST':

        cursor = db.cursor()
        input_studentid = request.form.get('student_id')
        input_instructorid = session['id']

        cursor.execute('CALL addAdvisor(%s, %s)', (input_studentid, input_instructorid))
        db.commit()
        cursor.close()

        return render_template('addadvisor.html')

    return render_template('addadvisor.html')

@app.route('/removestudentadvisor', methods=['GET','POST'])
def removeStudentAdvisor():

    if request.method == 'POST':

        cursor = db.cursor()
        input_studentid = request.form.get('student_id')
        input_instructorid = session['id']

        cursor.execute('CALL removeAdvisor(%s, %s)', (input_studentid, input_instructorid))
        db.commit()
        cursor.close()

        return render_template('removeadvisor.html')

    return render_template('removeadvisor.html')


@app.route('/checkroster', methods=['GET','POST'])
def checkroster():
    if request.method == 'GET':
        return render_template('checkroster.html')

    instructor_id = session['id']
    course_id = request.form['course_id']
    section_id = request.form['section_id']
    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()
    cursor.execute('CALL checkSectionRoster(%s, %s, %s, %s, %s)', (instructor_id, course_id, section_id, semester, year))

    data = cursor.fetchall()
    cursor.close()

    return render_template('resultscheckroster.html', data=data)

@app.route('/checksemesterroster', methods=['GET','POST'])
def checkSemesterRoster():
    if request.method == 'GET':
        return render_template('checksemesterroster.html')

    instructor_id = session['id']
    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()
    cursor.execute('CALL checkRoster(%s, %s, %s)', (instructor_id, semester, year))

    data = cursor.fetchall()
    cursor.close()

    return render_template('checksemesterrosterresults.html', data=data)

@app.route('/removestudentfromsection', methods=['GET','POST'])
def removeStudentFromSection():
    if request.method == 'GET':
        return render_template('removestudentfromsection.html')

    student_id = request.form['student_id']
    course_id = request.form['course_id']
    section_id = request.form['section_id']
    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()

    sql = "DELETE FROM takes WHERE ID = %s AND course_id = %s AND sec_id = %s AND semester = %s AND year = %s"
    cursor.execute(sql, (student_id, course_id, section_id, semester, year))
    
    db.commit()


    cursor.close()

    return render_template('removestudentfromsection.html')

@app.route('/addprereq', methods=['GET', 'POST'])
def addprereq():
    if request.method == 'GET':
        return render_template('addprereq.html')

    course_id = request.form['course_id']
    
    prereq_id = request.form['prereq_id']

    cursor = db.cursor()
    cursor.execute('CALL addPrereq(%s, %s)', (course_id, prereq_id))
    db.commit()
    cursor.close()

    return render_template('addprereq.html')



@app.route('/removeprereq')
def removeprereq():
    if request.method == 'GET':
        return render_template('removeprereq.html')

    course_id = request.form['course_id']
    prereq_id = request.form['prereq_id']

    cursor = db.cursor()
    cursor.execute('CALL removePrereq(%s, %s)', (course_id, prereq_id))
   
    db.commit()

    cursor.close()

    return render_template('removeprereq.html')


#student stuff
@app.route('/registerclass', methods=['GET','POST'])
def registerClass():

    if request.method == 'GET':
        return render_template('registerclass.html')

    student_id = session['id'] 
    course_id = request.form['course_id']
    section_id = request.form['section_id']
    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()

    cursor.execute('CALL classEnroll(%s, %s, %s, %s, %s)', (student_id, course_id, section_id, semester, year))
    db.commit()

    cursor.close()

    return render_template('registerclass.html')

@app.route('/dropsection', methods=['GET','POST'])
def dropSection():

    if request.method == 'GET':
        return render_template('dropsection.html')

    student_id = session['id'] 
    course_id = request.form['course_id']
    section_id = request.form['section_id']
    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()

    cursor.execute('CALL dropSection(%s, %s, %s, %s, %s)', (student_id, course_id, section_id, semester, year))
    db.commit()
    cursor.close()

    return render_template('dropsection.html')

@app.route('/finalgrades')
def finalGrades():

    student_id = session['id']

    cursor = db.cursor()

    sql = "SELECT course_id, sec_id, semester, year, grade FROM takes WHERE ID = %s"
    cursor.execute(sql, (student_id,))
    data = cursor.fetchall()

    cursor.close()

    return render_template('finalgrades.html', data=data)

@app.route('/checkbysemester', methods=['GET','POST'])
def checkBySemester():

    if request.method == 'GET':
        return render_template('checkbysemester.html')

    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()
    sql = "SELECT course_id, sec_id, semester, year FROM section WHERE semester = %s AND year = %s"
    cursor.execute(sql, (semester, year))

    data = cursor.fetchall()
    cursor.close()

    return render_template('checkbysemesterresults.html', data=data, semester=semester, year=year)

@app.route('/sectioninfo', methods=['GET', 'POST'])
def sectionInfo():

    if request.method == 'GET':
        return render_template('sectioninfo.html')

    course_id = request.form['course_id']
    section_id = request.form['section_id']
    semester = request.form['semester']
    year = request.form['year']

    cursor = db.cursor()

    cursor.execute('CALL sectionInfo(%s, %s, %s, %s)',(course_id, section_id, semester, year))

    data = cursor.fetchall()
    cursor.close()

    return render_template('sectioninforesults.html', data=data, course_id=course_id, section_id=section_id, semester=semester, year=year)

@app.route('/advisorinfo', methods=['GET'])
def advisorInfo():

    student_id = session['id']
    cursor = db.cursor()

    cursor.execute('CALL checkAdvisor(%s)', (student_id))
    data = cursor.fetchall()

    cursor.close()

    return render_template('advisorinfo.html', data=data)



