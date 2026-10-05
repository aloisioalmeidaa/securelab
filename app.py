import os
import sqlite3
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash


# Carrega as variáveis do arquivo .env
load_dotenv()


# Criação da aplicação Flask
app = Flask(__name__)

# Chave utilizada para proteger a sessão e os tokens CSRF
app.secret_key = os.getenv("SECRET_KEY")


# Proteção contra CSRF
csrf = CSRFProtect(app)


# Configurações de segurança da sessão
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Tempo máximo da sessão autenticada
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


# --------------------------------------------------
# BANCO DE DADOS
# --------------------------------------------------

def init_db():
    connection = sqlite3.connect("securelab.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS amostras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identificador TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL,
            observacao TEXT
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

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
            session.permanent = True

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Usuário ou senha inválidos."
        )

    return render_template("login.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    # Impede acesso ao dashboard sem autenticação
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return redirect(url_for("login"))


# --------------------------------------------------
# CABEÇALHOS HTTP DE SEGURANÇA
# --------------------------------------------------

@app.after_request
def add_security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'"
    )

    return response


# --------------------------------------------------
# INICIALIZAÇÃO DO BANCO
# --------------------------------------------------

init_db()


# --------------------------------------------------
# EXECUÇÃO DA APLICAÇÃO
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False)