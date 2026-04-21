from flask import Flask, render_template, request, redirect, url_for, session
import config
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = config.dbserver

app = Flask(__name__)
app.debug = True

app.secret_key = 'Epic Ben and Zoe Website'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
    msg = ''
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
        session['loggedin'] = True
        session['id'] = account[0] 
        session['username'] = account[1]
        return redirect(url_for('index'))
    else:
        msg = 'Incorrect username/password!'   

    return render_template('home.html', msg=msg)

@app.route('/login/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# Logout 
@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
