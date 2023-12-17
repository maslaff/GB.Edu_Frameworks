# Создать страницу, на которой будет форма для ввода имени и электронной почты,
# при отправке которой будет создан cookie-файл с данными пользователя,
# а также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка «Выйти», при нажатии на которую
# будет удалён cookie-файл с данными пользователя и произведено
# перенаправление на страницу ввода имени и электронной почты.

from flask import (
    Flask,
    request,
    make_response,
    render_template,
    flash,
    redirect,
    url_for,
)

app = Flask(__name__)

app.secret_key = "5f214cacbd30c2a0f17912ae0d5d8c16ae9812846221265e4"


@app.route("/")
def index():
    name = request.cookies.get("username")
    if name:
        return render_template("index.html", title="Страница сайта", uname=name)
    else:
        return redirect(url_for("login_get"))


@app.post("/login/")
def login_post():
    # session["username"] = request.form.get("username") or "NoName"
    form_uname = request.form.get("username")
    form_email = request.form.get("email")
    flash(f"User {form_uname} logged in", "success")
    response = make_response(redirect(url_for("index")))
    response.set_cookie("username", form_uname)
    response.set_cookie("email", form_email)
    return response
    # return redirect(url_for("index"))


@app.get("/login/")
def login_get():
    return render_template("login.html")


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
    app.run()
