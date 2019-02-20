from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_mysqldb import MySQL
from forms import RegisterForm
from db import Database
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/questions')
def employees():
    def db_query():
        db = Database()
        emps = db.list_users()
        return emps
    res = db_query()
    return render_template('questions.html', result=res, content_type='application/json')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form= RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name= form.name.data
        username=form.username.data
        email= form.email.data
        password =sha256_crypt.encrypt(str(form.password.data))
        
        db = Database()
        cur = db.con.cursor()
        cur.execute("INSERT INTO users (name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))
        # Commit to DB
        db.con.commit()

        # Close db connectons
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form= form)



@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        db= Database()
        cur = db.con.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    db= Database()
    cur = db.con.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM questions WHERE quiz_owner= %s", [session['username']])

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Questions Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()
@app.route('/questions/<int:id>', methods=['GET', 'POST'])
def question(id):
    return render_template('questions.html', id =id)

if __name__ == "__main__":
    app.secret_key='secret123'
    app.run( debug=True)
