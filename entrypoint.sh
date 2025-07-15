#!/bin/sh

# Executa os testes usando o comando 'make test'
echo "Running tests..."
make test

# Verifica o código de saída do comando 'make test'
if [ $? -ne 0 ]; then
   echo "Tests failed! Exiting container."
   exit 1
 fi

# echo "Tests passed! Starting application..."

# Inicia a aplicação Uvicorn
# Certifique-se de que 'store.app:app' é o caminho correto para sua aplicação
exec uvicorn store.app:app --host 0.0.0.0 --port 8000
