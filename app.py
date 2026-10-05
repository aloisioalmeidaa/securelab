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
# NOVA AMOSTRA
# --------------------------------------------------

@app.route("/amostras/nova", methods=["GET", "POST"])
def nova_amostra():

    # Somente usuários autenticados podem acessar
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    if request.method == "POST":

        identificador = request.form.get("identificador", "").strip()
        tipo = request.form.get("tipo", "").strip()
        data = request.form.get("data", "").strip()
        status = request.form.get("status", "").strip()
        observacao = request.form.get("observacao", "").strip()

        status_permitidos = {
            "Recebida",
            "Em análise",
            "Finalizada"
        }

        if (
            not identificador
            or not tipo
            or not data
            or status not in status_permitidos
        ):
            return render_template(
                "nova_amostra.html",
                error="Preencha os campos obrigatórios corretamente."
            )

        connection = sqlite3.connect("securelab.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO amostras
            (identificador, tipo, data, status, observacao)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                identificador,
                tipo,
                data,
                status,
                observacao
            )
        )

        connection.commit()
        connection.close()

        return redirect(url_for("dashboard"))

    return render_template("nova_amostra.html")

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    # Impede acesso ao dashboard sem autenticação
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    connection = sqlite3.connect("securelab.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            identificador,
            tipo,
            data,
            status,
            observacao
        FROM amostras
        ORDER BY id DESC
    """)

    amostras = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        amostras=amostras
    )


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