import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    TOTVS_AUTH_URL = "https://portal.topiconsultoria.com.br:8051/api/connect/token/"  # Verifique se está correto
    # 🔹 Token dura 5 minutos, então configuramos a expiração
    TOKEN_EXPIRATION_SECONDS = 300  
    REFRESH_TOKEN_EXPIRATION_SECONDS = 86400  # Refresh token dura 24h

    # 🔹 Tempo máximo de inatividade antes de deslogar (Ex: 30 min)
    MAX_INACTIVITY_TIME = 1800 

