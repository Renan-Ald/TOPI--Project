from flask import render_template, request, jsonify, session
import requests

# Definindo a URL base
BASE_API_URL = "https://portal.topiconsultoria.com.br:8051/api/framework/v1/consultaSQLServer/RealizaConsulta"
API_URL = "https://portal.topiconsultoria.com.br:8051/RMSRestDataServer/rest/RMSPRJ4728832Server"

def api_get(url):
    """Função genérica para realizar GET com Bearer Token."""
    token = session.get("access_token")
    if not token:
        return jsonify({"error": "Usuário não autenticado"}), 401
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    return response.json() if response.status_code == 200 else None

def obter_dados_apontamento():
    """Obtém os dados do apontamento baseado na coligada do usuário."""
    coligada = session.get("coligada")
    if not coligada:
        return jsonify({"error": "Coligada não encontrada na sessão"}), 401
    
    url = f"{BASE_API_URL}/APT.INT.004/0/T?parameters=CODCOLIGADA={coligada}"
    return api_get(url)

def apontamento_page():
    """Página de apontamento que obtém os dados e permite envio via POST."""
    coligada_data = obter_dados_apontamento()
    
    if request.method == "POST":
        token = session.get("access_token")
        if not token:
            return jsonify({"error": "Usuário não autenticado"}), 401
        
        payload = {
            "CODCOLIGADA": int(request.form.get("cod_coligada")),
            "CODAPONTAMENTO": int(request.form.get("cod_apontamento")),
            "CODVEN": request.form.get("cod_ven"),
            "CODPROJETO": int(request.form.get("cod_projeto")),
            "CODTAREFA": int(request.form.get("cod_tarefa")),
            "DATA": request.form.get("data"),
            "HRINI": f"{request.form.get('data')}T{request.form.get('hr_ini')}:00-03:00",
            "HRFIM": f"{request.form.get('data')}T{request.form.get('hr_fim')}:00-03:00",
            "HRINT": f"{request.form.get('data')}T{request.form.get('hr_int')}:00-03:00",
            "DESCRICAO": request.form.get("descricao"),
            "CODTB1FAT": request.form.get("cod_tb1fat")
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            return jsonify({"message": "Apontamento enviado com sucesso!"}), 200
        else:
            return jsonify({"error": "Erro ao enviar apontamento", "detalhes": response.text}), response.status_code
    
    return render_template("apontamento.html", coligada_data=coligada_data)
