import logging

from src.adapters.inbound.serverless.errors.business_exception_handler import BusinessExceptionHandler
from src.adapters.inbound.serverless.errors.default_exception_handler import DefaultExceptionHandler
from src.adapters.inbound.serverless.errors.key_error_exception import KeyErrorHandler
from src.adapters.inbound.serverless.errors.value_error_exception import ValueErrorHandler
from src.application.exceptions.business_exception import BusinessException


class GlobalExceptionHandler:
    _strategies = {
        ValueError: ValueErrorHandler(),
        KeyError: KeyErrorHandler(),
        BusinessException: BusinessExceptionHandler(),
    }
    _default_strategy = DefaultExceptionHandler()

    @staticmethod
    def handle_exception(exception, event):
        """
        Trata exceções usando a estratégia apropriada.

        :param exception: Exceção capturada.
        :param event: Evento recebido pela Lambda.
        :return: Dicionário no formato esperado pela AWS Lambda.
        """
        logging.error(f"Erro capturado: {exception}", exc_info=True)
        strategy = GlobalExceptionHandler._strategies.get(type(exception), GlobalExceptionHandler._default_strategy)
        return strategy.handle(exception, event)