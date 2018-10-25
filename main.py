from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '22316wsefwauwbfub'



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        

@app.before_request
def require_login():
    allowed_routes = ['login','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/')
def index():
    return render_template('login.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='Post':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist, error')
            return redirect ('/login')
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method =='POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        # TODO -validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/newpost')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html') 

@app.route('/newpost', methods=['GET', 'POST'])
def post():

        if request.method == 'POST':
            blog_name = request.form['title']
            blog_body = request.form['body']
            owner_id = User.query.filter_by(username=['username']).first()
            new_blog = Blog(blog_name, blog_body, owner_id) 
            db.session.add(new_blog)
            db.session.commit()
            return render_template('singleblogpost.html', blog=new_blog)
        
        return render_template('newpost.html')    
        

@app.route('/blog') 
def blog():
    blogs = Blog.query.all()

    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)

        return render_template('singleblogpost.html', blog=blog)

    else:
        blogs = Blog.query.all()

    return render_template('blog.html', title="Build a Blog", blogs=blogs)



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')


if __name__ == '__main__':


    app.run()