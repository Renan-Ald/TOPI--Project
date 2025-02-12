from flask import render_template, request, jsonify, session
import requests

API_URL = "https://portal.topiconsultoria.com.br:8051/RMSRestDataServer/rest/RMSPRJ4728832Server"

def apontamento_page():
    if request.method == "POST":
        # Recuperando o token da sessão
        token = session.get("access_token")
        if not token:
            return jsonify({"error": "Usuário não autenticado"}), 401

        # Capturando dados do formulário
        data = request.form.get("data")
        hr_ini = request.form.get("hr_ini")
        hr_fim = request.form.get("hr_fim")
        hr_int = request.form.get("hr_int")
        cod_coligada = request.form.get("cod_coligada")
        cod_apontamento = request.form.get("cod_apontamento")
        cod_ven = request.form.get("cod_ven")
        cod_projeto = request.form.get("cod_projeto")
        cod_tarefa = request.form.get("cod_tarefa")
        descricao = request.form.get("descricao")
        cod_tb1fat = request.form.get("cod_tb1fat")

        # Criando o payload para o POST
        payload = {
            "CODCOLIGADA": int(cod_coligada),
            "CODAPONTAMENTO": int(cod_apontamento),
            "CODVEN": cod_ven,
            "CODPROJETO": int(cod_projeto),
            "CODTAREFA": int(cod_tarefa),
            "DATA": data,
            "HRINI": f"{data}T{hr_ini}:00-03:00",
            "HRFIM": f"{data}T{hr_fim}:00-03:00",
            "HRINT": f"{data}T{hr_int}:00-03:00",
            "DESCRICAO": descricao,
            "CODTB1FAT": cod_tb1fat
        }

        # Criando os headers com o Bearer Token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # Enviando os dados via POST para a API
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return jsonify({"message": "Apontamento enviado com sucesso!"}), 200
        else:
            return jsonify({"error": "Erro ao enviar apontamento", "detalhes": response.text}), response.status_code

    return render_template("apontamento.html")
