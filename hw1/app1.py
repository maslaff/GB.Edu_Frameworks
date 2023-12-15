from flask import Flask, render_template

app = Flask(__name__)

contn = "Годнота"


@app.route("/")
@app.route("/main/")
def main():
    return render_template("main.html", title="Меню")


@app.route("/wear/")
def wear():
    return render_template("wear.html", title="Одежда")


@app.route("/boots/")
def boots():
    return render_template("boots.html", title="Обувь")


@app.route("/jacket/")
def jacket():
    return render_template("jacket.html", title="Куртец")


if __name__ == "__main__":
    app.run()
