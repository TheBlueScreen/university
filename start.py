from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Aryan:12341234@localhost/cedatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
hossein = User(username="Hossein", email="hossein@gmail.com", password="123321")
db.session.add(hossein)

db.session.add(
    News(title="canceled", content="nvlsjnsjlrvgnsrlvlsjns", category="class", date="3 december", author=hossein))
db.session.add(
    News(title="exist", content="nvlsjnsjlrvgrrrrrrrrrrrrrrsf!!!!nsrlvlsjns", category="place", date="4 december",
         author=aryan))
db.session.commit()


@app.route("/")
def home():
    news = News.query.all()
    return render_template("html.html", nw=news)


@app.route("/add-post", methods=["get"])
def newPost():
    return render_template("addPost.html")


@app.route("/login", methods=["get"])
def login():
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


@app.route("/add-post", methods=["post"])
def newPostPost():
    title = request.form['title']
    content = request.form['content']
    author = request.form['author']
    date = request.form['date']


    news = News(title=title, content=content,author = author , date = date
    )
    db.session.add(news)
    db.session.commit()
    return render_template("addPost.html")


if __name__ == '__main__':
    app.run(port=8080)
