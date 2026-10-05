import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        correct_username = os.getenv("APP_USERNAME")
        password_hash = os.getenv("APP_PASSWORD_HASH")

        if (
            username == correct_username
            and password_hash
            and check_password_hash(password_hash, password)
        ):
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Usuário ou senha inválidos."
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=False)