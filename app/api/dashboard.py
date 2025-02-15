import requests
from flask import render_template, session, request
from datetime import datetime, timedelta
from config import Config

# URL base para requisições
BASE_URL = "https://portal.topiconsultoria.com.br:8051/api/framework/v1/consultaSQLServer/RealizaConsulta/"

def get_mes_atual():
    """Retorna o primeiro e o último dia do mês atual."""
    hoje = datetime.today()
    primeiro_dia = hoje.replace(day=1).strftime("%Y-%m-%d")
    
    # Calcula o primeiro dia do próximo mês
    if hoje.month == 12:
        proximo_mes = datetime(hoje.year + 1, 1, 1)
    else:
        proximo_mes = datetime(hoje.year, hoje.month + 1, 1)
    
    # O último dia do mês atual é o dia anterior ao primeiro dia do próximo mês
    ultimo_dia = (proximo_mes - timedelta(days=1)).strftime("%Y-%m-%d")
    
    return primeiro_dia, ultimo_dia

def obter_dados_usuario():
    """Obtém os dados do usuário logado."""
    usuario = session.get("user")
    coligada = session.get("coligada")
    token = session.get("token")

    if usuario and coligada and token:
        url = f"{BASE_URL}APT.INT.003/0/T?parameters=CODCOLIGADA={coligada};USUARIO={usuario}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dados = response.json() 
            session["CODVEN"] = dados[0]["CODVEN"]
            return dados[0] if isinstance(dados, list) and dados else None
    return None

def obter_dados_periodo(data_de, data_ate):
    """Consulta API com as datas selecionadas."""
    usuario = session.get("user")
    coligada = session.get("coligada")
    token = session.get("token")

    if usuario and coligada and token:
        url = f"{BASE_URL}APT.INT.002/0/T?parameters=CODCOLIGADA={coligada};USUARIO={usuario};DATADE_D={data_de};DATAATE_D={data_ate}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
    return None

def dashboard():
    """Renderiza o dashboard com os dados e permite a seleção de datas."""
    dados_usuario = obter_dados_usuario()
    nome_usuario = dados_usuario.get("NOME", "Nome não disponível") if dados_usuario else "Erro ao carregar dados"

    # Obtém as datas, usando as do mês atual por padrão
    data_de = request.args.get("data_de")
    data_ate = request.args.get("data_ate")

    if not data_de or not data_ate:
        data_de, data_ate = get_mes_atual()

    dados_periodo = obter_dados_periodo(data_de, data_ate)

    return render_template(
        "dashboard.html",
        nome=nome_usuario,
        data_de=data_de,
        data_ate=data_ate,
        dados_periodo=dados_periodo
    )
