import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)

""" WTForm validation for registration form """


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField(
        "Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


""" WTForm validation for login form"""


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


""" WTForm validation for product recommendation form"""


class ProductForm(FlaskForm):
    product_name = StringField(
        "Product Name", validators=[DataRequired(), Length(min=3, max=50)])
    product_description = StringField(
        "Product Description",
        validators=[DataRequired(), Length(min=3, max=500)])
    product_link = StringField(
        "Product Link", validators=[DataRequired(), Length(min=10, max=1000)])
    product_image = StringField(
        "Product Image", validators=[DataRequired(), Length(min=10, max=200)])
    product_price = StringField(
        "Product Price", validators=[DataRequired(), Length(min=1, max=10)])
    submit = SubmitField("Recommend Product")


""" displays errors with forms """


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), "error")


""" Home Page"""


@app.route("/")
def home():
    return render_template("home.html")


""" register Page"""


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("home"))
    else:
        form = RegistrationForm()
        # register when logged in redirect
        if request.method == "POST" and form.validate_on_submit():
            # check if username already exists in db
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                flash("Username already exists")
                return redirect(url_for("register"))

            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password"))
            }
            mongo.db.users.insert_one(register)
            session["user"] = request.form.get("username").lower()
            flash("Registration Successful!")
            return redirect(url_for("profile", username=session["user"]))
        else:
            flash_errors(form)
        return render_template("register.html", form=form)


""" login Page"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))
    else:
        form = LoginForm()
        # logged when register in redirect
        if request.method == "POST" and form.validate_on_submit():
            # check if username exists in db
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                # ensure hashed password matches user input
                if check_password_hash(
                   existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                            request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
                else:
                    # invalid password match
                    flash("Incorrect Username and/or Password")
                    return redirect(url_for("login"))
            else:
                # username doesn't exist
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
    return render_template("login.html", title="Login", form=form)


""" Contact Page"""


@app.route("/contact")
def contact():
    if request.method == "POST":
        flash("Message Sent")
        return redirect(url_for("contact"))
    return render_template("contact.html")


""" Work article Page"""


@app.route("/work_article")
def work_article():
    return render_template("work_article.html")


""" Home decor article Page"""


@app.route("/home_decor")
def home_decor():
    return render_template("home_decor.html")


""" community recommendations Page"""


@app.route("/get_recommendations")
def get_recommendations():
    recommendations = list(mongo.db.recommendations.find())
    return render_template(
        "recommendations.html", recommendations=recommendations)


""" search bar function"""


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recommendations = list(mongo.db.recommendations.find(
        {"$text": {"$search": query}}))
    return render_template(
        "recommendations.html", recommendations=recommendations)


""" Profile Page"""


@app.route("/profile/", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        # grab the session user's username from db
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        if session["user"]:
            recommendations = list(mongo.db.recommendations.find())
        return render_template(
            "profile.html", username=username, recommendations=recommendations)
    return redirect(url_for("login"))


""" Logout function"""


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


""" Add recommendation Page"""


@app.route("/add_recommendation", methods=["GET", "POST"])
def add_recommendation():  # if user not in session
    if "user" not in session:
        return redirect(url_for("home"))
    else:
        form = ProductForm()
        if request.method == "POST" and form.validate_on_submit():
            is_hidden_gem = "on" if request.form.get(
                "is_hidden_gem") else "off"
            recommendations = {
                "category_name": request.form.get("category_name"),
                "product_name": request.form.get("product_name"),
                "product_description": request.form.get("product_description"),
                "product_link": request.form.get("product_link"),
                "product_image": request.form.get("product_image"),
                "product_price": request.form.get("product_price"),
                "is_hidden_gem": is_hidden_gem,
                "author": session["user"]
            }
            mongo.db.recommendations.insert_one(recommendations)
            flash("Product Recommended!")
            return redirect(url_for("get_recommendations"))
        else:
            flash_errors(form)
        categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "add_recommendation.html", categories=categories, form=form)


""" Edit recommendation Page"""


@app.route("/edit_product/<recommendation_id>", methods=["GET", "POST"])
def edit_recommendation(recommendation_id):
    if "user" not in session:
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            is_hidden_gem = "on" if request.form.get(
                "is_hidden_gem") else "off"
            submit = {
                "category_name": request.form.get("category_name"),
                "product_name": request.form.get("product_name"),
                "product_description": request.form.get("product_description"),
                "product_link": request.form.get("product_link"),
                "product_image": request.form.get("product_image"),
                "product_price": request.form.get("product_price"),
                "is_hidden_gem": is_hidden_gem,
                "author": session["user"]
            }
            mongo.db.recommendations.update(
                {"_id": ObjectId(recommendation_id)}, submit)
            flash("Product Updated!")

        recommendation = mongo.db.recommendations.find_one(
            {"_id": ObjectId(recommendation_id)})
        categories = mongo.db.categories.find().sort("category_name", 1)
        return render_template(
            "edit_recommendation.html",
            recommendation=recommendation, categories=categories)


""" Delete recommendation function"""


@app.route("/delete_recommendation/<recommendation_id>")
def delete_recommendation(recommendation_id):
    mongo.db.recommendations.remove({"_id": ObjectId(recommendation_id)})
    flash("Recommendation Succesfully Removed")
    return redirect(url_for("get_recommendations"))


""" Admin category page"""


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


""" Add category function"""


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if "user" not in session:
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            category = {
                "category_name": request.form.get("category_name")
            }
            mongo.db.categories.insert_one(category)
            flash("New Category Added")
            return redirect(url_for("get_categories"))

        return render_template("add_categories.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
