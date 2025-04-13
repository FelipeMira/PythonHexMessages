from src.application.exceptions.business_exception import BusinessException
from src.application.exceptions.errors import Errors
from src.application.ports.inbound.process_message_use_case import ProcessMessage
from src.application.ports.outbound.send_message import SendMessage
from threading import Lock

class ProcessMessageService(ProcessMessage):
    _instance = None
    _lock = Lock()

    def __new__(cls, send_messages: list[SendMessage]):
        """
        Garante que apenas uma instância da classe seja criada.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ProcessMessageService, cls).__new__(cls)
                cls._instance.send_messages = send_messages
        return cls._instance

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