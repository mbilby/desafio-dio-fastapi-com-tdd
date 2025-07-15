FROM python:3.13.4-alpine3.22

# Define o diretório de trabalho no contêiner
WORKDIR /TDD

# Instala as dependências do Python
RUN apk update && apk add --no-cache \
    make \
    build-base \
    bash \
    mongodb-tools \
    # Adicione outras dependências que seu app precise (ex: postgresql-dev para psycopg2)
    # && rm -rf /var/lib/apk/lists/* # No alpine, o --no-cache já cuida disso
    && rm -rf /var/cache/apk/* # Limpa o cache para reduzir o tamanho da imagem

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o entrypoint para o container
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copia o restante da aplicação
COPY . /TDD

# Expõe a porta padrão do FastAPI/Uvicorn
EXPOSE 8000

# Define PYTHONPATH globalmente
ENV PYTHONPATH=/TDD

# Define o script como o ENTRYPOINT do contêiner
ENTRYPOINT ["./entrypoint.sh"]

# CMD agora pode ser vazio ou conter argumentos padrão se o entrypoint aceitar
CMD []
