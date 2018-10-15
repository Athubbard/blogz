from flask import Flask, request, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/newpost', methods=['GET', 'POST'])
def post():
      
    if request.method == 'POST':
        blog_name = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_name, blog_body) 
        db.session.add(new_blog)
        db.session.commit()


    
       
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

app.run()