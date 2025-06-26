import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

class Config:
    SECRET_KEY = 'c84f1f3a348e4c5bbacb9d31e1428a5c6e9e59dc3ad24f04b68b77598c1ecdd4'
    TOTVS_AUTH_URL = "https://portal.topiconsultoria.com.br:8051/api/connect/token/"
    TOKEN_EXPIRATION_SECONDS = 1800  
    REFRESH_TOKEN_EXPIRATION_SECONDS = 86400
    MAX_INACTIVITY_TIME = 1800 

    # 🔐 Flask-Session configuração
    #SESSION_TYPE = 'redis'
    #SESSION_PERMANENT = False
    #SESSION_USE_SIGNER = True

    SESSION_COOKIE_SECURE = False  
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Recomendo comentar SESSION_COOKIE_DOMAIN temporariamente até validar o funcionamento
    # SESSION_COOKIE_DOMAIN = '192.168.18.233'

    # Redis
    #SESSION_REDIS = Redis(host='localhost', port=6379)
