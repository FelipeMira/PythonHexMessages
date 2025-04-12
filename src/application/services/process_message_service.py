from src.application.exceptions.business_exception import BusinessException
from src.application.exceptions.errors import Errors
from src.application.ports.inbound.process_message_use_case import ProcessMessage
from src.application.ports.outbound.send_message import SendMessage


class ProcessMessageService(ProcessMessage):
    def __init__(self, send_messages: list[SendMessage]):
        """
        Serviço para processar mensagens.

        :param send_messages: Lista de implementações de SendMessage.
        """
        self.send_messages = send_messages

    def run(self, message):
        """
        Processa a mensagem fornecida.

        :param message: Instância de Message.
        :raises BusinessException: Caso ocorra algum erro de validação ou envio.
        """
        if not message.message_attributes:
            Errors.throw_business_exception(Errors.ERROR_MESSAGE_WITHOUT_ATTRIBUTES)

        if not message.text:
            Errors.throw_business_exception(Errors.ERROR_MESSAGE_WITHOUT_TEXT)

        x_type = message.message_attributes.get("x-type")

        if not x_type:
            Errors.throw_business_exception(Errors.ERROR_X_TIPO_NOT_FOUND)

        sender = next(
            (s for s in self.send_messages if s.canQueue(x_type)),
            None
        )

        if not sender:
            raise BusinessException(Errors.ERROR_OUT_PORT_NOT_FOUND)

        sender.send(message)