import logging

from app.src.adapters.inbound.serverless.awslambda.errors.business_exception_handler import BusinessExceptionHandler
from app.src.adapters.inbound.serverless.awslambda.errors.default_exception_handler import DefaultExceptionHandler
from app.src.adapters.inbound.serverless.awslambda.errors.key_error_exception import KeyErrorHandler
from app.src.adapters.inbound.serverless.awslambda.errors.value_error_exception import ValueErrorHandler
from app.src.application.exceptions.business_exception import BusinessException


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