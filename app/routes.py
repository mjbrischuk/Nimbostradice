from app import app
from app import db, bcrypt
from app.models import User

from flask import request
from flask import url_for
from flask import render_template
from flask import session
from flask import redirect
from flask import send_from_directory

from sqlalchemy import or_

from markupsafe import escape

@app.route("/hello")
 # example of request.args + escaping injected html
def hello():
    print("request.args")
    print(request.args)
    print("request.form")
    print(request.form)
    name = request.args.get('name','Flask')
    print(name)
    return f"Hello, {escape(name)}!"

@app.route('/hello/<name>')
def helloName(name=None):
    print(name)
    return render_template('hello.html', person=name)

@app.get('/login')
def login_get():
    print(session)
    return render_template('login.html',)

@app.post('/login')
def login_post():
# request.form is a dict -> form['userInput']=='asdf'  ,  form['pwInput']=='zxcv'
    user_id = request.form.get('userInput')
    password = request.form.get('pwInput')

    user = User.query.filter(
        or_(User.username == user_id, User.email == user_id)
    ).first()

    if user and bcrypt.check_password_hash(user.password, password):
        if request.form.get('rememberMeCheck'):
            session.permanent = True
        session['user_id'] = user.id
        redirect_url = url_for('helloName', name=user.username)
        return redirect(redirect_url)
    else:
        # todo: add a flash message explaining the login failed
        return render_template('login.html', error='Invalid username or password')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_get'))

@app.route('/register')
def register_get():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register_post():
    if not app.config['REGISTRATION_OPEN']:
        return 'Registration is closed', 403

    username = request.form['username']
    email = request.form['email']
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login_get'))
@app.route('/test')
def test():
    return render_template('test.html',)

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')