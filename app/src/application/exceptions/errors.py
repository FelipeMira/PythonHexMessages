from app.src.application.exceptions.business_exception import BusinessException

class Errors:
    ERROR_PERSIST_PORT_NOT_FOUND = "Database not found"
    ERROR_MESSAGE_WITHOUT_TEXT = "Message without text"
    ERROR_MESSAGE_WITHOUT_ATTRIBUTES = "Message without attributes"
    ERROR_MESSAGE_WITHOUT_ATTRIBUTE_QUEUE_URL = "Message without attribute queueUrl"
    ERROR_X_TIPO_NOT_FOUND = "x-tipo not found"
    ERROR_OUT_PORT_NOT_FOUND = "Out port not found"

    @staticmethod
    def throw_business_exception(message: str):
        """
        Lança uma BusinessException com a mensagem fornecida.
        :param message: Mensagem de erro.
        """
        raise BusinessException(message)