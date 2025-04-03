# Usa a imagem oficial do Python
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para dentro do contêiner
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000 do contêiner (o Nginx redirecionará da 8080 para 5000)
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "run.py"]
