from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Aryan:12341234@localhost/cedatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hello-i-am-aryan'
db = SQLAlchemy(app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(550), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    news = db.relationship('News', backref='author', lazy='dynamic')


db.drop_all()
db.create_all()

aryan = User(username="Aryan", email="ayan@gmail.com", password="123123")

db.session.add(aryan)
db.session.commit()

# hossein = User(username="Hossein", email="hossein@gmail.com", password="123321")
# db.session.add(hossein)
#
# db.session.add(
#     News(title="canceled", content="nvlsjnsjlrvgnsrlvlsjns", category="class", date="3 december", author=hossein))
db.session.add(
    News(title="Why Amazon and Google just can't get along",
         content="google amazongoogle amazongoogle amazongoogle amazon ", category="place", date="4 december",
         author=aryan))
db.session.commit()


@app.route("/")
def home():
    news = News.query.all()
    return render_template("html.html", nw=news)


@app.route("/add-post", methods=["get"])
def newPost():
    return render_template("addPost.html")


@app.route("/userProfile", methods=["get", "post"])
def userprofile():
    return render_template("userprofile.html")


@app.route("/login", methods=["get"])
def login():
    print("testing!!!")
    return render_template("login.html")


@app.route("/about", methods=["get"])
def about():
    return render_template("about.html")


@app.route("/news", methods=["get"])
def completeNews():
    return render_template("news.html")


@app.route("/register", methods=["get"])
def register():
    return render_template("register.html")


@app.route('/news/<id>')
def post(id):
    return render_template('news.html', n=News.query.get(id))


@app.route("/add-post", methods=["post"])
def newPostPost():
    title = request.form['title']
    content = request.form['content']
    date = request.form['date']
    category = request.form['category']
    author = User.query.get(1)
    news = News(title=title, content=content, date=date, category=category, author=author)
    db.session.add(news)
    db.session.commit()
    return render_template("addPost.html")


@app.route("/register", methods=["post"])
def logout():
    return "kar mikone?"
    session.pop('username', None)
    session.pop('password', None)
    return "Logout shod"


@app.route('/login', methods=["post"])
def loginPost():
    # if request.method == 'GET':
    #     return render_template('login.html')
    username = request.form['userName']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return render_template("login.html", session=session)
    session['username'] = username
    session['password'] = password
    return render_template("userProfile.html", session=session)


@app.route('/profile', methods=["post"])
def profile():
    if ('username' in session):
        return render_template("userProfile.html", session=session)
    else:
        return redirect("http://127.0.0.1:8080/login")


@app.route("/register", methods=["post"])
def addMember():
    userName = request.form['newUserName']
    email = request.form['email']
    passWord = request.form['password']
    user = User(username=userName, email=email, password=passWord)
    exists = db.session.query(User.id).filter_by(username=userName).scalar() is not None
    if exists:
        return 'tekrari'
    else:
        db.session.add(user)
        db.session.commit()

        session['username'] = userName
        session['email'] = email
        session['password'] = passWord

        return render_template("register.html", session=session)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
