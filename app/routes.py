from flask import Blueprint
from app.api.auth import login, logout
from app.api.dashboard import dashboard
from app.api.services import salvar_coligada,salvar_codapontamento
from app.api.apontamento import apontamento_page, apontamento_page_edit, apontamento_page_delete ,get_apontamentos,criar_apontamento, editar_apontamento

routes = Blueprint("routes", __name__)

routes.route("/login", methods=["GET", "POST"])(login)
routes.route("/dashboard")(dashboard)
routes.route("/logout")(logout)
routes.route("/salvar-coligada", methods=["GET", "POST"])(salvar_coligada)
routes.route("/apontamento", methods=["GET", "POST"])(apontamento_page)  
routes.route("/apontamento_edit", methods=["GET", "PUT"])(apontamento_page_edit)
routes.route("/apontamento_delete", methods=["GET", "DELETE"])(apontamento_page_delete)  
routes.route('/get_apontamentos', methods=['GET'])(get_apontamentos)
routes.route('/criar_apontamento', methods=['POST'])(criar_apontamento)
routes.route('/editar_apontamento', methods=['POST'])(editar_apontamento)
routes.route("/salvar-codapontamento", methods=["GET", "POST"])(salvar_codapontamento)