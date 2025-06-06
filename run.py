from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
#from app import create_app

#app = create_app()

#if _name_ == "_main_":
    #app.run(ssl_context=("certs/cert.pem", "certs/key.pem"), host="0.0.0.0", port=5000, debug=True)