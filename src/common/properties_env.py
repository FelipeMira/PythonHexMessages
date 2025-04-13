import os
from dotenv import load_dotenv

# Define o caminho base para os arquivos .env
BASE_ENV_PATH = ".././configuration/resources"
# Obtém o ambiente atual (ex.: local, dev, hom, prod, test)
current_env = os.getenv("APP_ENV", "local")

# Constrói o caminho do arquivo .env correspondente
env_file = os.path.join(BASE_ENV_PATH, f".env.{current_env}")

# Carrega o arquivo .env
load_dotenv(env_file)
print(f"Carregando variaveis de ambiente do arquivo: {env_file}")

# Exemplo de uso
queue_url = os.getenv("QUEUE_URL")
print(f"Queue URL carregado: {queue_url}")

queue_error_url = os.getenv("QUEUE_URL_ERROR")
print(f"Queue Error URL carregado: {queue_error_url}")
x_type_error = os.getenv("AWS_SQS_OUT_QUEUES_ERROR_X_TYPE")

queue_alert_url = os.getenv("QUEUE_URL_ALERT")
print(f"Queue Alert URL carregado: {queue_alert_url}")
x_type_alert = os.getenv("AWS_SQS_OUT_QUEUES_ALERT_X_TYPE")

dynamodb_table_name = os.getenv("DYNAMODB_TABLE_NAME")
print(f"DynamoDB Table Name carregado: {dynamodb_table_name}")