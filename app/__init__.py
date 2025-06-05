from flask import Flask, request, session, redirect, url_for
import datetime
import requests
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def verificar_sessao():
    """Middleware para verificar sessão do usuário e atualizar token se necessário."""
    #print("Sessão atual:", session)

    rotas_livres = ["routes.login", "routes.salvar_coligada", "static"]  # Rotas abertas

    # Se a requisição for para uma rota livre, não verifica sessão
    if request.endpoint in rotas_livres:
        return  

    # Se a sessão não tiver token ou refresh_token, redireciona para o login
    if "token" not in session or "refresh_token" not in session:
        return redirect(url_for("routes.login"))

    # Verifica tempo de inatividade
    tempo_atual = datetime.datetime.now().timestamp()
    if "ultima_atividade" in session:
        tempo_inativo = tempo_atual - session["ultima_atividade"]
        if tempo_inativo > Config.MAX_INACTIVITY_TIME:
            session.clear()
            return redirect(url_for("routes.login"))

    # Atualiza timestamp da última atividade
    session["ultima_atividade"] = tempo_atual

    # Se o token expirou, tenta renovar
    if not atualizar_token():
        return redirect(url_for("routes.login"))

def atualizar_token():
    """Tenta renovar o token de autenticação."""
    token_expira_em = session.get("token_expira_em")
    refresh_token = session.get("refresh_token")

    if not token_expira_em or not refresh_token:
        return False  # Se não houver refresh_token, não pode renovar

    tempo_atual = datetime.datetime.now().timestamp()

    if tempo_atual >= token_expira_em:  # Se o token expirou
        payload = {"refresh_token": refresh_token}
        try:
            response = requests.post(Config.TOTVS_AUTH_URL, json=payload, timeout=5)

            if response.status_code == 200:
                dados = response.json()
                session["token"] = dados.get("access_token")  # Atualiza token
                session["token_expira_em"] = tempo_atual + Config.TOKEN_EXPIRATION_SECONDS
                return True
            else:
                session.clear()
                return False
        except requests.RequestException:
            session.clear()
            return False

    return True  # Se o token ainda for válido

def create_app():
    """Cria e configura o aplicativo Flask."""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)
    JWTManager(app)

    from app.routes import routes
    app.register_blueprint(routes)

    # Middleware é adicionado APÓS as rotas serem registradas
    app.before_request(verificar_sessao)

    return app
