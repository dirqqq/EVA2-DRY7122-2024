import pyotp
import sqlite3
import hashlib
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

db_name = 'test.db'

@app.route('/')
def index():
    return 'Welcome to the hands-on lab for an evolution of password systems!'

######################################### Plain Text #########################################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            PASSWORD  TEXT    NOT NULL);''')
    conn.commit()
    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)", 
                  (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username has been registered."
    print('username: ', request.form['username'], ' password: ', request.form['password'])
    return "Signup success"

def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?", (username,))
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == password

@app.route('/login/v1', methods=['POST'])
def login_v1():
    error = None
    if verify_plain(request.form['username'], request.form['password']):
        error = 'Login success'
    else:
        error = 'Invalid username/password'
    return error

######################################### Password Hashing #########################################################
@app.route('/signup/v2', methods=['POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            HASH      TEXT    NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)", 
                  (request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username has been registered."
    print('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "Signup success"

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USER_HASH WHERE USERNAME = ?", (username,))
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v2', methods=['POST'])
def login_v2():
    error = None
    if verify_hash(request.form['username'], request.form['password']):
        error = 'Login success'
    else:
        error = 'Invalid username/password'
    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7050, ssl_context='adhoc')
