import os

from cs50 import SQL
from datetime import date
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure UPLOAD_FOLDER
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproject.db")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?",
                      request.form.get("username"))
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        # verify if they provided username
        if not username:
            return apology("must provide username", 400)
        elif len(rows) == 1:
            return apology("username already exists", 400)
        # verify if they provided password
        elif not password:
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # create a new user with users's input
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   username, generate_password_hash(password))

        # Redirect user to login form
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/account")
@login_required
def account():
    # query database for all recipes
    recipes = db.execute(
        "SELECT * FROM recipes WHERE user_id = ?", session["user_id"])

    # query database for all tips
    tips = db.execute(
        "SELECT * FROM tips WHERE user_id = ?", session["user_id"])
    return render_template("account.html", recipes=recipes, tips=tips)


@app.route("/share", methods=["GET", "POST"])
@login_required
def share():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        title = request.form.get("title")
        recipe = request.form.get("recipe")
        ingredients = request.form.get("ingredients")

        # check input title and recipe
        if not title or not recipe or not ingredients:
            return apology("must provide title, recipe & ingredients", 403)

        # check if the post request has the file part
        if 'file' not in request.files:
            return apology("no file part", 403)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return apology("no selected file", 403)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # create a new recipe with user's input
        db.execute("INSERT INTO recipes (title, ingredients, recipe, image, user_id) VALUES (?, ?, ?, ?, ?)",
                   title, ingredients, recipe, filename, session["user_id"])

        return redirect("/recipes")

    else:
        return render_template("share.html")


@app.route("/sharetips", methods=["GET", "POST"])
@login_required
def sharetips():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        title = request.form.get("title")
        post = request.form.get("post")
        now = date.today()

        # check input title and recipe
        if not title or not post:
            return apology("must provide title, recipe & ingredients", 403)

        # create a new recipe with user's input
        db.execute("INSERT INTO tips (title, post, user_id, time) VALUES (?, ?, ?, ?)",
                   title, post, session["user_id"], now)

        return redirect("/")

    else:
        return render_template("sharetips.html")


@app.route("/recipes", methods=["GET"])
def recipes():
    # query database for all recipes
    recipes = db.execute("SELECT * FROM recipes")
    return render_template("recipes.html", recipes=recipes)


@app.route("/tips", methods=["GET"])
def tips():
    # query database for all tips
    tips = db.execute(
        "SELECT tips.id, title, post, username, time FROM tips JOIN users ON users.id = tips.user_id")

    return render_template("tips.html", tips=tips)


@app.route("/list", methods=["GET"])
def list():
    return render_template("list.html")
