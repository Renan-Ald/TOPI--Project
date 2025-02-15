from flask import Blueprint
from app.api.auth import login, logout
from app.api.dashboard import dashboard
from app.api.services import salvar_coligada
from app.api.apontamento import apontamento_page ,get_apontamentos,criar_apontamento

routes = Blueprint("routes", __name__)

routes.route("/", methods=["GET", "POST"])(login)
routes.route("/dashboard")(dashboard)
routes.route("/logout")(logout)
routes.route("/salvar-coligada", methods=["GET", "POST"])(salvar_coligada)
routes.route("/apontamento", methods=["GET", "POST"])(apontamento_page)  # Adicionando a rota de apontamento
routes.route('/get_apontamentos', methods=['GET'])(get_apontamentos)
routes.route('/criar_apontamento', methods=['POST'])(criar_apontamento)
