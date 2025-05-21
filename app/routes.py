from flask import Blueprint
from app.api.auth import login, logout
from app.api.dashboard import dashboard
from app.api.services import salvar_coligada, salvar_codapontamento
from app.api.apontamento import (
    apontamento_page,
    apontamento_page_edit,
    apontamento_page_delete,
    get_apontamentos,
    criar_apontamento,
    editar_apontamento
)

routes = Blueprint("routes", __name__)

# Autenticação
routes.route("/login", methods=["GET", "POST"])(login)
routes.route("/logout", methods=["GET"])(logout)

# Dashboard
routes.route("/dashboard", methods=["GET"])(dashboard)

# Serviços
routes.route("/salvar-coligada", methods=["GET", "POST"])(salvar_coligada)
routes.route("/salvar-codapontamento", methods=["GET", "POST"])(salvar_codapontamento)

# Página principal do apontamento (criação e listagem)
routes.route("/apontamento", methods=["GET", "POST"])(apontamento_page)

# Edição de apontamento
# GET para carregar formulário, PUT para salvar (usando JS com _method=PUT ou formulário real PUT via fetch)
routes.route("/apontamento_edit", methods=["GET", "PUT"])(apontamento_page_edit)

# Exclusão de apontamento
routes.route("/apontamento_delete", methods=["GET", "DELETE"])(apontamento_page_delete)

# API endpoints
routes.route("/get_apontamentos", methods=["GET"])(get_apontamentos)
routes.route("/criar_apontamento", methods=["POST"])(criar_apontamento)
routes.route("/editar_apontamento", methods=["GET", "POST", "PUT"])(editar_apontamento)
