from login_app import app
from flask import render_template, redirect, request, session, flash
from login_app.models.logins import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    hashed_password = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : hashed_password
    }
    User.save(data)
    id = User.get_user_by_email(data)
    session['user_id'] = id
    return redirect('/success')

@app.route("/login", methods =['POST'])
def login():
    data = {
        'email' : request.form['email']
    } 
    login_validation = User.validate_login(data)

    if not login_validation:
        redirect('/')
    
    user_in_db = User.get_user_by_email(data)
    print("***************************************")
    print(user_in_db.password)
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash('Invalid email/password.', "login_email")
            return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/success')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    logged_in_user = User.get_user_by_id(data)
    if logged_in_user == False:
        return redirect('/')
    return render_template('/dashboard.html', user = logged_in_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')