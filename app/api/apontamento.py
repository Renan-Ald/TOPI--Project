from flask import render_template, request, jsonify, session
import requests

# Definindo a URL base
BASE_API_URL = "https://portal.topiconsultoria.com.br:8051/api/framework/v1/consultaSQLServer/RealizaConsulta/"
API_URL = "https://portal.topiconsultoria.com.br:8051/RMSRestDataServer/rest/RMSPRJ4728832Server"

def projetos():
    """Obtém a lista de projetos do usuário logado."""
    usuario = session.get("user")
    coligada = session.get("coligada")
    token = session.get("token")
    
    if usuario and coligada and token:
        url = f"{BASE_API_URL}APT.INT.004/0/T?parameters=CODCOLIGADA={coligada}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dados = response.json()
            return dados if isinstance(dados, list) else []
    return []

def obter_dados_tarefa():  
    """Obtém a lista de tarefas do usuário logado."""
    usuario = session.get("user")
    coligada = session.get("coligada")
    token = session.get("token")

    if usuario and coligada and token:
        url = f"{BASE_API_URL}APT.INT.005/0/T?parameters=CODCOLIGADA={coligada}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            dados = response.json()
            return dados if isinstance(dados, list) else []
    return []

def obter_apontamentos(cod_projeto):
    """Obtém os apontamentos filtrados pelo CODPROJETO."""
    usuario = session.get("user")
    coligada = session.get("coligada")
    token = session.get("token")

    if usuario and coligada and token:
        url = f"{BASE_API_URL}APT.INT.006/0/T?parameters=CODCOLIGADA={coligada};CODPROJETO={cod_projeto}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json() if isinstance(response.json(), list) else []
    return []

def obter_apontamento(codcoligada, codapontamento):
    """Obtém os apontamentos filtrados pelo CODPROJETO."""
    usuario = session.get("user")
    coligada = session.get("coligada")
    token = session.get("token")

    if usuario and coligada and token:
        url = f"{API_URL}/{coligada}$_${codapontamento}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json() if isinstance(response.json(), list) else []
    return []

def get_apontamentos():
    """Endpoint para retornar apontamentos com base no CODPROJETO."""
    cod_projeto = request.args.get("cod_projeto")
    if not cod_projeto:
        return jsonify({"error": "CODPROJETO não fornecido"}), 400
    
    apontamentos = obter_apontamentos(cod_projeto)
    return jsonify(apontamentos)      

def apontamento_page():
    """Renderiza a página de apontamento com os dados do projeto e tarefa."""
    dados_projeto = projetos()
    dados_tarefa = obter_dados_tarefa()

    return render_template('apontamento.html', dados_projeto=dados_projeto, dados_tarefa=dados_tarefa)

def apontamento_page_edit():
    """Renderiza a página de apontamento com os dados do projeto e tarefa."""
    dados_projeto = projetos()
    dados_tarefa = obter_dados_tarefa()
    get_apont= obter_apontamento()
    print(get_apont)
    codcoligada = request.args.get('codcoligada')
    codapontamento = request.args.get('codapontamento')
    # Aqui você pode carregar os dados com base nos parâmetros recebidos

    return render_template(
        'apontamento_edit.html',
        get_apont=get_apont,
        dados_projeto=dados_projeto,
        dados_tarefa=dados_tarefa,
        codcoligada=codcoligada,
        codapontamento=codapontamento
    )

# Novo método para criar um apontamento
def criar_apontamento():
    """Cria um novo apontamento com os dados recebidos do frontend."""
    codven= session.get("CODVEN")
    print("codigoven"+ codven)
    if request.method == "POST":
        token = session.get("token")
        if not token:
            return jsonify({"error": "Usuário não autenticado"}), 401
        
        # Recebendo os dados do formulário
        payload = {
            "ZMDAPONTAMENTO": [{
            "CODCOLIGADA": int(session.get("coligada")),
            "CODVEN": codven,
            "CODPROJETO": int(request.form.get("cod_projeto")),
            "CODTAREFA": int(request.form.get("cod_tarefa")),
            "DATA": request.form.get("data"),
            "HRINI": f"{request.form.get('data')}T{request.form.get('hr_ini')}:00-03:00",
            "HRFIM": f"{request.form.get('data')}T{request.form.get('hr_fim')}:00-03:00",
            "HRINT": f"{request.form.get('data')}T{request.form.get('hr_int')}:00-03:00",
            "DESCRICAO": request.form.get("descricao"),
            "CODTB1FAT": int(request.form.get("cod_apontamento"))           

        }]
        }
        print("Payload do Apontamento:")
        print(payload)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            return jsonify({"message": "Apontamento enviado com sucesso!"}), 200
        else:
            return jsonify({"error": "Erro ao enviar apontamento", "detalhes": response.text}), response.status_code
        
# Novo método para editar um apontamento
def editar_apontamento():
    """Edita um sapontamento com os dados recebidos do frontend."""
    codven= session.get("CODVEN")
    print("codigoven"+ codven)
    if request.method == "PUT":
        token = session.get("token")
        if not token:
            return jsonify({"error": "Usuário não autenticado"}), 401
        
        # Recebendo os dados do formulário
        payload = {
            "ZMDAPONTAMENTO": [{
            "CODCOLIGADA": int(session.get("coligada")),
            "CODVEN": codven,
            "CODPROJETO": int(request.form.get("cod_projeto")),
            "CODTAREFA": int(request.form.get("cod_tarefa")),
            "DATA": request.form.get("data"),
            "HRINI": f"{request.form.get('data')}T{request.form.get('hr_ini')}:00-03:00",
            "HRFIM": f"{request.form.get('data')}T{request.form.get('hr_fim')}:00-03:00",
            "HRINT": f"{request.form.get('data')}T{request.form.get('hr_int')}:00-03:00",
            "DESCRICAO": request.form.get("descricao"),
            "CODTB1FAT": int(request.form.get("cod_apontamento"))
        }]
        }
        print("Payload do Apontamento:")
        print(payload)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            return jsonify({"message": "Apontamento editado com sucesso!"}), 200
        else:
            return jsonify({"error": "Erro ao editar apontamento", "detalhes": response.text}), response.status_code
def obter_apontamento():
    """Obtém os detalhes de um apontamento específico para edição."""
    token = session.get("token")
    cod_coligada = session.get("coligada")
    cod_apontamento = session.get("codapontamento")
    if not token:
        return jsonify({"error": "Usuário não autenticado"}), 401

    # Monta a URL correta
    url = f"{API_URL}/{cod_coligada}$_${cod_apontamento}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        apontamento = response.json()
        return apontamento
    else:
        print(response.status_code)
        return jsonify({"error": "Erro ao obter apontamento", "detalhes": response.text}), response.status_code
    
def apontamento_page_delete():  
    """Exclui apontamento selecionado"""
    usuario = session.get("user")
    token = session.get("token")
    codcoligada = request.args.get('codcoligada')
    codapontamento = request.args.get('codapontamento')


    if usuario and codcoligada and token and codapontamento:
        url = f"{API_URL}/{codcoligada}$_${codapontamento}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            return render_template('dashboard.html')
        else:
            return jsonify({"error": "Erro ao excluir apontamento", "detalhes": response.text}), response.status_code
        
