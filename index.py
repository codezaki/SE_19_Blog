from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from re import escape
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<Task %r>' % self.id
    
@app.route("/")
def hello_world():
    posts = Post.query.all()
    return render_template("profile_page.html", posts = posts, str = str, escape = escape, enumerate = enumerate)

@app.route("/createpost", methods = ["POST"])
def submit_post():
    post = Post(content = request.form['content'], title = request.form['title'])
    db.session.add(post)
    db.session.commit()
    return redirect('/')

@app.route("/delete/<id>", methods = ['POST'])
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')

@app.route("/editpost/<id>", methods = ['POST'])
def edit_post(id):
    Post.query.filter_by(id=id).update({
        'title':request.form['title'],
        'content':request.form['content']
    })
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)