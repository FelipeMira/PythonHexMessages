from abc import ABC
import logging
from src.application.ports.outbound.send_message import SendMessage


class BaseQueue(SendMessage, ABC):
    def __init__(self, x_type: str, queue_url: str, sqs_client, message_out_mapper):
        """
        Classe base para envio de mensagens para filas SQS.

        :param x_type: Tipo da fila (x-type).
        :param queue_url: URL da fila SQS.
        :param sqs_client: Cliente SQS configurado.
        :param message_out_mapper: Mapper para converter mensagens para o formato SQS.
        """
        self.x_type = x_type
        self.queue_url = queue_url
        self.sqs_client = sqs_client
        self.message_out_mapper = message_out_mapper

    def can_queue(self, x_type: str) -> bool:
        """
        Verifica se o tipo da fila corresponde ao esperado.

        :param x_type: Tipo da fila a ser verificado.
        :return: True se o tipo corresponder, False caso contrário.
        """
        return x_type == self.x_type

    def send(self, message):
        """
        Envia uma mensagem para a fila SQS.

        :param message: Instância de Message a ser enviada.
        """
        try:
            send_request = self.message_out_mapper.message_to_send_message_request(
                message, self.queue_url
            )
            self.sqs_client.send_message(**send_request)
            logging.info(f"Mensagem enviada: {message.text} para a fila {self.queue_url}")
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem: {e}")