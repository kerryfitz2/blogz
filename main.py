from flask import request, redirect, render_template, flash, session
from models import User, Blog
from app import app, db
#from datetime import datetime

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    print (session)
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            print(session)
            return redirect('/blog')
        else:
            flash('User password incorrect or user does not exist', 'error')
            
    return render_template('login.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form ['password']
        verify = request.form ['verify']

        existing_user = User.query.filter_by(email = email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')

        else:
            return '<h1>Duplicate User</h1>'

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

@app.route('/blog', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()
    return render_template('blog.html',title="My Blogs", 
        blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    blogs = Blog.query.all()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        #pub_date = datetime.utcnow()
        if title != "" and body !="":
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return render_template('blog.html',title="Add a Blog Entry", blogs=blogs)
        else:
            flash('Please enter conent for your blog title and body','error')

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()