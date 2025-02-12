import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    TOTVS_AUTH_URL = "https://portal.topiconsultoria.com.br:8051/api/connect/token/"  # Verifique se está correto

