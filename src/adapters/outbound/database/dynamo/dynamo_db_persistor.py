import logging

from src.adapters.outbound.database.dynamo.config.dynamo_db_config import DynamoDBConfig
from src.adapters.outbound.database.dynamo.mappers.message_out_db_mapper import MessageOutDBMapper
from src.application.ports.outbound.persistor_message import PersistorMessage
from botocore.exceptions import BotoCoreError, ClientError

from src.common.properties_env import dynamodb_table_name


class DynamoDBPersistor(PersistorMessage):
    def __init__(self):
        """
        Inicializa o persistor com a tabela DynamoDB.

        :param table_name: Nome da tabela DynamoDB.
        """
        self.table_name = dynamodb_table_name
        self.dynamodb_client = DynamoDBConfig().get_client()

    def can_database(self, message):
        """
        Verifica se a mensagem pode ser persistida no banco de dados.

        :param message: Mensagem a ser verificada.
        :return: True se a mensagem pode ser persistida, False caso contrário.
        """
        return True

    def save(self, message):
        """
        Salva a mensagem no DynamoDB.

        :param message: Mensagem a ser salva.
        :raises Exception: Caso ocorra um erro ao salvar a mensagem.
        """
        try:
            item = MessageOutDBMapper.map(message)
            self.dynamodb_client.put_item(
                TableName=self.table_name,
                Item=item,
            )
            logging.info(f"Mensagem {item.get('id')} salva com sucesso no DynamoDB.")
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Erro ao salvar a mensagem no DynamoDB: {e}")