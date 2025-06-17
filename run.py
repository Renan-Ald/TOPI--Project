from waitress import serve
from app import create_app

app = create_app()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5050)

#from waitress import serve
#from app import create_app

#app = create_app()

#if _name_ == "_main_":
    #serve(ssl_context=("certs/cert.pem", "certs/key.pem"), host="0.0.0.0", port=5000, debug=True)