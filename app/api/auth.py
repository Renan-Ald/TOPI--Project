import requests
from flask import request, session, redirect, url_for, flash, render_template
from config import Config

def autenticar_usuario(usuario, senha):
    payload = {"username": usuario, "password": senha}
    response = requests.post(Config.TOTVS_AUTH_URL, json=payload)
    #print("print do json")
    #print(response.json())
    if response.status_code == 200:
        session["token"] = response.json().get("access_token") 
        print(session["token"])
        return response.json()  # Retorna o token
    return None

def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        resultado = autenticar_usuario(usuario, senha)

        if resultado:
            print(session)
            session["user"] = usuario  # Armazena na sessão
            
            return redirect(url_for("routes.dashboard"))
        else:
            flash("Usuário ou senha inválidos", "danger")

    return render_template("login.html")

def logout():
    session.pop("user", None)
    return redirect(url_for("routes.login"))
