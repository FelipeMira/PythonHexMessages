import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, NoCredentialsError
from src.common.properties_env import current_env  # Importa o current_env


class DynamoDBConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DynamoDBConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Configuração para o DynamoDB.

        :param environment: Ambiente atual (ex.: 'local' ou 'prod').
        """
        if not hasattr(self, "_initialized"):
            self.environment = current_env  # Usa o current_env importado
            self.dynamodb_client = None
            self._initialized = True  # Garante que o __init__ seja executado apenas uma vez

    def initialize_client(self):
        """
        Inicializa o cliente DynamoDB com base no ambiente.
        """
        try:
            if self.environment == "local":
                self.dynamodb_client = boto3.client(
                    "dynamodb",
                    endpoint_url="http://localhost:4566",
                    aws_access_key_id="teste",
                    aws_secret_access_key="teste",
                    region_name="sa-east-1",
                    config=Config(retries={"max_attempts": 10, "mode": "standard"}),
                )
            else:
                self.dynamodb_client = boto3.client(
                    "dynamodb",
                    region_name="sa-east-1",
                    config=Config(retries={"max_attempts": 10, "mode": "standard"}),
                )
        except (BotoCoreError, NoCredentialsError) as e:
            raise Exception(f"Erro ao inicializar o cliente DynamoDB: {e}")

    def get_client(self):
        """
        Retorna o cliente DynamoDB inicializado.
        :return: Cliente DynamoDB.
        """
        if not self.dynamodb_client:
            self.initialize_client()
        return self.dynamodb_client