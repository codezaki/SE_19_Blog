from json import JSONEncoder
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from re import escape
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'd9c6926142d33bc4099f47d04d411ce8eb8f760d958884471fbf7a8752e8ee56'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class Post(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model, UserMixin, SerializerMixin):
    serialize_rules = ('-posts.user', )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref="user")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def signup():
    print(request)
    return render_template("signup_page.html", passwords_match=True, username_taken=False)


@app.route("/login")
def login():
    return render_template("login_page.html")


@app.route("/signup_attempt", methods=['POST'])
def signup_attempt():
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    password_repeat = request.form['password_repeat']

    user = User.query.filter_by(username=username).first()

    passwords_match = True
    username_taken = False

    # check password repeat
    if password != password_repeat:
        passwords_match = False
    if user:
        username_taken = True
    if passwords_match and not username_taken:
        hash_password = generate_password_hash(password, method='sha256')
        newUser = User(username=username, password=hash_password, name=name)
        db.session.add(newUser)
        db.session.commit()
        return redirect('/login')
    return redirect(url_for('signup', passwords_match=passwords_match, username_taken=username_taken))


@app.route("/login_attempt", methods=['POST'])
def login_attempt():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    has_error = False
    if not user or not check_password_hash(user.password, password):
        has_error = True
        return redirect(url_for('login', has_error=has_error))
    login_user(user, remember=True)
    return redirect(url_for('profile'))


@app.route("/profile")
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    res = []
    name_of_user = current_user.name

    for post in posts:
        res.append(post.to_dict())

    return render_template("profile_page.html", posts=res, str=str, escape=escape, jsonify=JSONEncoder().encode, user=current_user, name_of_user=name_of_user)


@app.route("/createpost", methods=["POST"])
@login_required
def submit_post():
    post = Post(content=request.form['content'],
                title=request.form['title'], user_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    return redirect('/profile')


@app.route("/delete/<id>", methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.user_id != current_user.id:
        return
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/profile')


@app.route("/editpost/<id>", methods=['POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.user_id != current_user.id:
        return
    Post.query.filter_by(id=id).update({
        'title': request.form['title'],
        'content': request.form['content']
    })
    db.session.commit()
    return redirect('/profile')


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/homepage")
def homepage():
    posts = Post.query.all()  # To keep them in chronological order
    posts.reverse()
    return render_template('/homepage.html', posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
