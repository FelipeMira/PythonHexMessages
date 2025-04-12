import logging

from src.adapters.inbound.message.config.sqs_config import SqsConfig
from src.adapters.inbound.message.sqs.sqs_input_adapter import SQSInputAdapter
from src.adapters.inbound.message.mappers.message_in_mapper import MessageInMapper
from src.adapters.outbound.message.sqs_output_alert import SQSOutputAlert
from src.adapters.outbound.message.sqs_output_error import SQSOutputError
from src.application.services.process_message_service import ProcessMessageService

class Application:
    """
    Classe para inicializar e executar o serviço.
    """

    @staticmethod
    def start():
        """
        Inicializa as dependências e inicia o listener do SQS.
        """
        logging.basicConfig(level=logging.INFO)

        # Instancia o mapeador de mensagens
        message_in_mapper = MessageInMapper()

        # Instancia as portas de saída
        sqs_output_alert = SQSOutputAlert()
        sqs_output_error = SQSOutputError()

        # Instancia o serviço de processamento de mensagens com as portas de saída
        process_message = ProcessMessageService([sqs_output_alert, sqs_output_error])

        # Cria o adaptador SQS
        sqs_adapter = SQSInputAdapter(process_message, message_in_mapper)

        # Inicia o listener
        logging.info("Iniciando o listener do SQS...")
        sqs_adapter.listen_to_sqs_queue()