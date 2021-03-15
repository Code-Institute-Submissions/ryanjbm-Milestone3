import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)
logged_in = "False"


def validate_form(form, collection):

    #variables
    max_name = 20
    max_productdescription = 50
    max_productlink = 200
    max_productimage = 200
    max_productprice = 1

    if collection == 'recommend':
        if not form['product_name'] or len(form['product_name']) > max_name:
            flash(
                'Product Name must not be empty or more than {} characters'
                .format(max_name)
            )
        return flash


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/our_recommendations")
def our_recommendations():
    return render_template("our_recommendations.html")


@app.route("/date_article")
def date_article():
    return render_template("date_article.html")


@app.route("/get_recommendations")
def get_recommendations():
    recommendations = list(mongo.db.recommendations.find())
    return render_template("recommendations.html", recommendations=recommendations)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")  # add default
    recommendations = list(mongo.db.recommendations.find(
        {"$text": {"$search": query}}))
    return render_template("recommendations.html", recommendations=recommendations)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return render_template("home.html")
    else:

        # register when logged in redirect
        if request.method == "POST":
            # check if username already exists in db
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                flash("Username already exists")
                return redirect(url_for("register"))

            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password"))
            }
            mongo.db.users.insert_one(register)

            # put the new user into 'session' cookie
            session["user"] = request.form.get("username").lower()
            flash("Registration Successful!")
            return redirect(url_for("profile", username=session["user"]))
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return render_template("home.html")
    else:

        # logged when register in redirect
        if request.method == "POST":
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
        return render_template("login.html")


@app.route("/profile/", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return render_template("home.html")
    else:

        # grab the session user's username from db
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        if session["user"]:
            recommendations = list(mongo.db.recommendations.find())
            return render_template("profile.html", username=username, recommendations=recommendations)

        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_recommendation", methods=["GET", "POST"])
def add_recommendation():  # if user not in session
    if "user" not in session:
        return render_template("home.html")
    else:
        if request.method == "POST":
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

        categories = mongo.db.categories.find().sort("category_name", 1)
        return render_template("add_recommendation.html", categories=categories)


@app.route("/edit_product/<recommendation_id>", methods=["GET", "POST"])
def edit_recommendation(recommendation_id):
    if "user" not in session:
        return render_template("home.html")
    else:
        if request.method == "POST":
            is_hidden_gem = "on" if request.form.get("is_hidden_gem") else "off"
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
        return render_template("edit_recommendation.html", recommendation=recommendation, categories=categories)


@app.route("/delete_recommendation/<recommendation_id>")
def delete_recommendation(recommendation_id):
    mongo.db.recommendations.remove({"_id": ObjectId(recommendation_id)})
    flash("Recommendation Succesfully Removed")
    return redirect(url_for("get_recommendations"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if "user" not in session:
        return render_template("home.html")
    else:
        if request.method == "POST":
            category = {
                "category_name": request.form.get("category_name")
            }
            mongo.db.categories.insert_one(category)
            flash("New Category Added")
            return redirect(url_for("get_categories"))

        return render_template("add_categories.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Succesfully Updated")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_categories.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
