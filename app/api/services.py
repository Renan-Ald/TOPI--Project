import requests
from flask import request, session, redirect, url_for, flash, render_template,jsonify
from config import Config


def salvar_coligada():
    dados = request.get_json()  # Recebe os dados do frontend
    coligada = dados.get('coligada')

    if coligada:
        session['coligada'] = coligada  # Salva a coligada na sessão
        return jsonify({"message": "Coligada salva com sucesso!"}), 200
    else:
        return jsonify({"message": "Coligada não fornecida"}), 400

def salvar_codapontamento():
    dados = request.get_json()  # Recebe os dados do frontend
    codapontamento = dados.get('codapontamento')

    if codapontamento:
        session['codapontamento'] = codapontamento 
        print("codigo apont" + codapontamento) # Salva a coligada na sessão
        return jsonify({"message": "Apontamento salva com sucesso!"}), 200
    else:
        return jsonify({"message": "Apontamento não fornecida"}), 400