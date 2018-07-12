from flask import request, redirect, render_template, flash, session
from models import User, Blog
from app import app, db
from sqlalchemy import desc

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    print (session)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/blog')
        else:
            flash('User password incorrect or user does not exist', 'error')
            
    return render_template('login.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form ['password']
        verify = request.form ['verify']

        existing_user = User.query.filter_by(username = username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')

        else:
            return '<h1>Duplicate User</h1>'

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

@app.route('/blog', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(username=session['username']).first()
    blogs = Blog.query.filter_by(owner=owner).order_by(desc(Blog.pub_date)).all()
    return render_template('blog.html',title="My Blogs", 
        blogs=blogs, owner=owner)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    owner = User.query.filter_by(username =session['username']).first()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        #pub_date = datetime.utcnow()
        if title != "" and body !="":
            new_post = Blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            blog = Blog.query.filter_by(id=new_post.id, owner=owner).first() 
            return render_template('entry.html', blog=blog, owner=owner)
           
        else:
            flash('Please enter conent for your blog title and body','error')

    return render_template('newpost.html')

@app.route('/entry', methods=['GET'])
def view_entry():
    owner = User.query.filter_by(username =session['username']).first()
    id = request.args.get('blog')
    blog = Blog.query.filter_by(owner=owner, id=id).first()
    return render_template('entry.html', blog=blog, owner=owner)

if __name__ == '__main__':
    app.run()