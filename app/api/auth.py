import requests
import time
from flask import request, session, redirect, url_for, flash, render_template
from config import Config
import datetime
# Função para autenticar o usuário e armazenar tokens na sessão
def autenticar_usuario(usuario, senha):
    payload = {"username": usuario, "password": senha}
    response = requests.post(Config.TOTVS_AUTH_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        session["token"] = data.get("access_token") 
        session["refresh_token"] = data.get("refresh_token")  
        session["token_expira_em"] = int(time.time()) + 1800  # 300 segundos (5 minutos)
        session["ultima_atividade"] = int(time.time())  # Atualiza atividade
        return data  

    return None
def verificar_inatividade():
    """Verifica se o usuário ficou inativo por mais de 30 minutos."""
    tempo_atual = datetime.datetime.now()
    ultimo_acesso = session.get("ultimo_acesso")

    if ultimo_acesso:
        ultimo_acesso = datetime.datetime.strptime(ultimo_acesso, "%Y-%m-%d %H:%M:%S")
        diferenca = (tempo_atual - ultimo_acesso).total_seconds()
        
        if diferenca > 1800:  # 30 minutos de inatividade
            session.clear()  # Remove sessão do usuário
            return redirect(url_for("routes.login"))

    session["ultimo_acesso"] = tempo_atual.strftime("%Y-%m-%d %H:%M:%S")

def atualizar_token():
    """Verifica e atualiza o token se necessário."""
    import requests
    from config import Config

    token_expira_em = session.get("token_expira_em")
    refresh_token = session.get("refresh_token")

    if token_expira_em and refresh_token:
        tempo_atual = datetime.datetime.now().timestamp()
        print(token_expira_em)
        if tempo_atual >= token_expira_em:  # Se o token expirou
            payload = {"refresh_token": refresh_token}
            response = requests.post(Config.TOTVS_REFRESH_URL, json=payload)

            if response.status_code == 200:
                dados = response.json()
                session["token"] = dados.get("access_token")
                session["token_expira_em"] = tempo_atual + 1800  # Atualiza a expiração
                return True
            else:
                session.clear()  # Se falhar, desloga o usuário
                return redirect(url_for("routes.login"))

    return True
# Função para requisições protegidas
def requisicao_protegida(endpoint):
    verificar_inatividade()  # Verifica se está inativo antes de continuar

    if not atualizar_token():
        return redirect(url_for("routes.login"))

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(f"{Config.API_BASE_URL}/{endpoint}", headers=headers)
    
    return response.json()

# Rota de login
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        resultado = autenticar_usuario(usuario, senha)

        if resultado:
            session["user"] = usuario  # Armazena usuário na sessão
            return redirect(url_for("routes.dashboard"))
        else:
            flash("Usuário ou senha inválidos", "danger")

    return render_template("login.html")

# Rota de logout
def logout():
    session.clear()
    flash("Você saiu da conta", "info")
    return redirect(url_for("routes.login"))
