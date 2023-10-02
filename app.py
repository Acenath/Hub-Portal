import random
from flask import Flask, render_template, jsonify,request,redirect,url_for,session
from flask_wtf import FlaskForm
from flask_mysqldb import MySQL
import MySQLdb.cursors
from weather import main as get_weather
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired
import datetime
import MySQLdb

app = Flask(__name__)

app.secret_key = 'very_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'murat33'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

count_id = 1


class QuestionForm(FlaskForm):
    options = RadioField('Options: ', validators=[DataRequired()], default=1)
    submit = SubmitField('Next')



@app.route('/', methods=['GET', 'POST'])
def index():
    data_1,data_2,data_3 = None, None, None
    if request.method == 'POST':
        city = request.form['CityName']
        if city == "":
            return render_template('index.html')
        data_1, data_2, data_3 = get_weather(city)
    return render_template('index.html',data_1 = data_1,data_2 = data_2, data_3 = data_3)


@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        username = request.form['Username']
        password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Username = % s AND Password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['Username'] = user['Username']
            session['Score'] = user.get('Score')
            message = 'Logged in successfully !'
            return render_template('index.html', message = message)
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message,session = session)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form and 'Password_check' in request.form:
        username = request.form['Username']
        password = request.form['Password']
        password_check = request.form['Password_check']
        name = request.form['Name']
        score = 0
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE Username = % s and Name = % s', (username, name, ))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not username or not password or not name or not password_check:
            message = 'Please fill out the form !'
        elif password != password_check:
            message = "Your password couldn't be confirmed !"
        else:
            cursor.execute(f'INSERT INTO users VALUES (Null,% s,% s, % s,% s)', (name,username, password,score, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('signup.html', message = message)

@app.route('/logout')
def logout():
    session['loggedin'] = False
    session['id'] = None
    session['Username'] = None
    return render_template("index.html")

@app.route("/exam", methods=["GET","POST"])
def exam():
    username = session['Username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE Username = % s', (username, ))
    user = cursor.fetchone()

    cursor.execute('SELECT * FROM questions ORDER BY q_id', ())
    q = cursor.fetchall()

    random_number = random.randint(0, len(q) - 1)
    print(f'Before the post: {random_number}')



    if request.method == 'POST':
        option = request.form['button']
        answer = q[random_number].get('ans')
        if option == answer:
            session['Score'] += 10
            cursor.execute(f"UPDATE Users SET Score= %s WHERE Username= %s",(session['Score'],username, ))
            mysql.connection.commit()
            return redirect(url_for('exam'))


    return render_template('exam.html', q = q, random_number = random_number, user = user)


@app.route('/pre_exam',methods = ['GET','POST'])
def pre_exam():
    return render_template('pre_exam.html')

@app.route('/scoreboard')
def scoreboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id,name,Score FROM users ORDER BY Score DESC')
    users = cursor.fetchall()
    return render_template('scoreboard.html',users = users)



if __name__ == '__main__':
    app.run()