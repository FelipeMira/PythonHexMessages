import logging

from src.adapters.inbound.message.sqs.sqs_input_adapter import SQSInputAdapter
from src.adapters.inbound.message.mappers.message_in_mapper import MessageInMapper
from src.adapters.inbound.serverless.awslambda.lambda_handler import LambdaHandler
from src.adapters.inbound.serverless.mappers.event_in_mapper import EventToMessageMapper
from src.adapters.outbound.database.dynamo_db_persistor import DynamoDBPersistor
from src.adapters.outbound.message.sqs_output_alert import SQSOutputAlert
from src.adapters.outbound.message.sqs_output_error import SQSOutputError
from src.application.ports.inbound.process_message_use_case import ProcessMessage
from src.application.ports.outbound.persistor_message import PersistorMessage
from src.application.services.process_message_service import ProcessMessageService

class Application:
    """
    Classe para inicializar e executar o serviço.
    """
    @staticmethod
    def _create_process_message_service() -> ProcessMessage:
        """Cria e retorna a instância do ProcessMessageService."""
        sqs_output_alert = SQSOutputAlert()
        sqs_output_error = SQSOutputError()
        persist_output   = DynamoDBPersistor()
        return ProcessMessageService([sqs_output_alert, sqs_output_error], [persist_output])

    @staticmethod
    def start():
        """
        Inicializa as dependências e inicia o listener do SQS.
        """
        logging.basicConfig(level=logging.INFO)

        # Instancia o mapeador de mensagens
        message_in_mapper = MessageInMapper()

        # Instancia o serviço de processamento de mensagens com as portas de saída
        process_message = Application._create_process_message_service()

        # Cria o adaptador SQS
        sqs_adapter = SQSInputAdapter(process_message, message_in_mapper)

        # Inicia o listener
        logging.info("Iniciando o listener do SQS...")
        sqs_adapter.listen_to_sqs_queue()

    @staticmethod
    def lambda_handler(event, context):
        """
        Handler padrão da Lambda que inicializa as dependências e processa o evento.
        """
        logging.basicConfig(level=logging.INFO)
        process_message_service = Application._create_process_message_service()
        lambda_handler = LambdaHandler(
            event_in_mapper=EventToMessageMapper(),
            process_message=process_message_service
        )
        result = lambda_handler.handle(event, context)
        logging.info(f"Resultado do processamento: {result}")
        return result