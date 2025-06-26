from flask import Flask, request, session, redirect, url_for
import datetime
import requests
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_session import Session  # <-- Importante
from hashids import Hashids

hashids = Hashids(salt="sua_senha_super_secreta", min_length=10)
def verificar_sessao():
    print("Request endpoint:", request.endpoint)
    rotas_livres = ["routes.login", "routes.salvar_coligada", "static", "routes.salvar_codapontamento"]

    if request.endpoint in rotas_livres:
        return  

    if "token" not in session or "refresh_token" not in session:
        return redirect(url_for("routes.login"))

    tempo_atual = datetime.datetime.now().timestamp()
    if "ultima_atividade" in session:
        tempo_inativo = tempo_atual - session["ultima_atividade"]
        if tempo_inativo > Config.MAX_INACTIVITY_TIME:
            session.clear()
            return redirect(url_for("routes.login"))

    session["ultima_atividade"] = tempo_atual

    if not atualizar_token():
        return redirect(url_for("routes.login"))

def atualizar_token():
    token_expira_em = session.get("token_expira_em")
    refresh_token = session.get("refresh_token")

    if not token_expira_em or not refresh_token:
        return False

    tempo_atual = datetime.datetime.now().timestamp()

    if tempo_atual >= token_expira_em:
        payload = {"refresh_token": refresh_token}
        try:
            response = requests.post(Config.TOTVS_AUTH_URL, json=payload, timeout=5)
            if response.status_code == 200:
                dados = response.json()
                session["token"] = dados.get("access_token")
                session["token_expira_em"] = tempo_atual + Config.TOKEN_EXPIRATION_SECONDS
                return True
            else:
                session.clear()
                return False
        except requests.RequestException:
            session.clear()
            return False

    return True

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)
    JWTManager(app)

    #Session(app)  # <-- Habilita o server-side session aqui

    from app.routes import routes
    app.register_blueprint(routes)

    app.before_request(verificar_sessao)
    app.jinja_env.globals['hashids'] = hashids
    return app
