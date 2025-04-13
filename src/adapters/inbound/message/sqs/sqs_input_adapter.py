import logging

from botocore.exceptions import ClientError

from src.adapters.inbound.message.sqs.config import SqsConfig
from src.adapters.inbound.message.sqs.mappers.message_in_mapper import MessageInMapper
from src.application.ports.inbound.process_message_use_case import ProcessMessage
from src.common.properties_env import queue_url  # Importa o current_env

class SQSInputAdapter:
    """
    Adaptador de entrada para receber mensagens do SQS.
    """

    def __init__(self, process_message: ProcessMessage, message_in_mapper: MessageInMapper):
        """
        Inicializa o adaptador com as dependências necessárias.

        :param process_message: Caso de uso para processar mensagens.
        :param message_in_mapper: Mapper para converter mensagens AWS para o domínio.
        :param sqs_client: Cliente SQS configurado.
        :param queue_url: URL da fila SQS.
        """
        logging.info("Inicializando o SQSInputAdapter.")
        self.process_message = process_message
        self.message_in_mapper = message_in_mapper
        self.sqs_client = SqsConfig().get_client()
        self.queue_url = queue_url
        logging.info(f"SQSInputAdapter inicializado com queue_url={self.queue_url}.")

    def listen_to_sqs_queue(self):
        """
        Escuta mensagens da fila SQS e as processa.
        """
        logging.info("Iniciando a escuta da fila SQS.")
        while True:
            try:
                logging.debug("Aguardando mensagens na fila...")
                response = self.sqs_client.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=20,
                    MessageAttributeNames=["All"]  # Garante que todos os atributos sejam retornados
                )

                messages = response.get('Messages', [])

                for raw_message in messages:
                    receipt_handle = raw_message['ReceiptHandle']
                    body = raw_message['Body']
                    headers = raw_message.get('MessageAttributes', {})

                    logging.info(f"Processando mensagem: {body}")
                    logging.debug(f"Headers da mensagem: {headers}")

                    domain_message = self.message_in_mapper.aws_to_domain(
                        {"Payload": body}, headers
                    )

                    try:
                        logging.info("Executando o processamento da mensagem.")
                        self.process_message.run(domain_message)
                        self.sqs_client.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=receipt_handle
                        )
                        logging.info("Mensagem processada e excluida com sucesso da fila.")
                    except Exception as e:
                        logging.error(f"Erro ao processar a mensagem: {e}", exc_info=True)

            except ClientError as e:
                logging.error(f"Erro ao conectar ao SQS: {e}", exc_info=True)
            except Exception as e:
                logging.error(f"Erro inesperado ao escutar a fila: {e}", exc_info=True)