from app import app
from flask import request
from flask import url_for
from markupsafe import escape
from flask import render_template
from flask import session
from flask import redirect

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
    print("request.form: ")
    print(request.form)
    print(session)
    session['userInput'] = request.form['userInput']
    if request.form.get('rememberMeCheck'):
        session.permanent = True
    print(session)

    redirect_url = url_for('helloName', name=request.form.get('userInput'))
    return redirect(redirect_url)
    # if valid_login(request.form['userInput'],
    #                request.form['pwInput']):
    #     return log_the_user_in(request.form['userInput'])
    # else:
    #     error = 'Invalid username/password'
    #     # the code below is executed if the request method
    #     # was GET or the credentials were invalid
    #    return render_template('login.html', error=error)


@app.route('/test')
def test():
    return render_template('test.html',)