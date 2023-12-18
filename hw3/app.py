from flask import (
    Flask,
    request,
    make_response,
    render_template,
    flash,
    redirect,
    url_for,
)

from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User
from forms import LoginForm

app = Flask(__name__)

app.secret_key = "5f214cacbd30c2a0f17912ae0d5d8c16ae9812846221265e4"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB created!")


@app.route("/")
def index():
    name = request.cookies.get("email")
    if name:
        return render_template("index.html", title="Страница сайта", uname=name)
    else:
        return redirect(url_for("login"))


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # users = User.query.all()
        # print(users)

        # session["username"] = request.form.get("username") or "NoName"
        form_email = request.form.get("email")
        form_password = request.form.get("password")
        usr_d = User.query.filter(User.email == form_email).first()
        if usr_d and check_password_hash(usr_d.password, form_password):
            flash(f"User {form_email} logged in", "success")
            response = make_response(redirect(url_for("index")))
            # response.set_cookie("username", form_uname)
            response.set_cookie("email", form_email)
            return response

        flash("Bad email or password", "warning")
        return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/registration/", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        # session["username"] = request.form.get("username") or "NoName"
        form_fname = request.form.get("first_name")
        form_lname = request.form.get("last_name")
        form_email = request.form.get("email")
        form_password = request.form.get("password")

        usr = User(
            first_name=form_fname,
            last_name=form_lname,
            email=form_email,
            password=generate_password_hash(form_password),
        )
        db.session.add(usr)
        db.session.commit()
        print(f"User {form_fname} {form_lname} registered")

        flash(f"User {form_email} registered", "success")
        response = make_response(redirect(url_for("login")))
        # response.set_cookie("user_email", form_email)

        return response
        # return redirect(url_for("index"))
    else:
        return render_template("registration.html")


@app.route("/logout/")
def logout():
    name = request.cookies.get("username")
    response = make_response(redirect(url_for("index")))
    response.delete_cookie("username")
    response.delete_cookie("email")
    flash(f"User {name} logged out", "success")
    return response


@app.errorhandler(404)
def page_not_found(e):
    context = {
        "title": "Страница не найдена",
        "url": request.base_url,
    }
    return render_template("404.html", **context), 404


if __name__ == "__main__":
    # init_db()
    app.run(debug=True)
