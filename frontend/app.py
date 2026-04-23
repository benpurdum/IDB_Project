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


if __name__ == '__main__':
    app.run(debug=True)
