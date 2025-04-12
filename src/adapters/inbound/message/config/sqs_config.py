import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, NoCredentialsError
from src.common.properties_env import current_env  # Importa o current_env


class SqsConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SqsConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Configuração para o SQS.

        :param environment: Ambiente atual (ex.: 'local' ou 'prod').
        """
        if not hasattr(self, "_initialized"):
            self.environment = current_env  # Usa o current_env importado
            self.sqs_client = None
            self._initialized = True  # Garante que o __init__ seja executado apenas uma vez

    def initialize_client(self):
        """
        Inicializa o cliente SQS com base no ambiente.
        """
        try:
            if self.environment == "local":
                self.sqs_client = boto3.client(
                    "sqs",
                    endpoint_url="http://localhost:4566",
                    aws_access_key_id="teste",
                    aws_secret_access_key="teste",
                    region_name="sa-east-1",
                    config=Config(retries={"max_attempts": 10, "mode": "standard"}),
                )
            else:
                self.sqs_client = boto3.client(
                    "sqs",
                    region_name="sa-east-1",
                    config=Config(retries={"max_attempts": 10, "mode": "standard"}),
                )
        except (BotoCoreError, NoCredentialsError) as e:
            raise Exception(f"Erro ao inicializar o cliente SQS: {e}")

    def get_client(self):
        """
        Retorna o cliente SQS inicializado.
        :return: Cliente SQS.
        """
        if not self.sqs_client:
            self.initialize_client()
        return self.sqs_client