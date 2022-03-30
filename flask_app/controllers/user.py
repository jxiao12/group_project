from os import stat
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.order import Order

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html', order=Order.get_all())
    data ={
        'id': session['user_id']
    }
    return render_template('index.html', order=Order.get_all(),
                            user=User.get_by_id(data))

@app.route('/login')
def logins():
    return render_template("login.html")

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    
    return redirect('/')

@app.route('/register')
def register():
    return render_template("register.html", state=states)

@app.route('/register',methods=['POST'])
def registers():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "address": request.form['address'],
        "city": request.form['city'],
        "state": request.form['state'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/') 

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/personal/<int:id>', methods=['GET'])
def edit_account(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":id
    }
    return render_template("account.html", user=User.get_by_id(data), state=states, orders=Order.get_all())

@app.route('/update/account',methods=['POST'])
def update_company():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session["user_id"]
    }
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "address": request.form["address"],
        "city": request.form["city"],
        "state": request.form["state"],
        "id": session["user_id"],
        "password": User.get_by_id(data).password
    }
    User.update(data)
    return redirect('/')

@app.route('/favorite_list',methods=['GET'])
def get_favorite():
    if 'user_id' not in session:
        return redirect('/')
    print(session)
    print(request.form)